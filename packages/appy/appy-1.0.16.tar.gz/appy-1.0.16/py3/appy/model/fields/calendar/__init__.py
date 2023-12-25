#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2023 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import types
from DateTime import DateTime
from persistent import Persistent
from BTrees.IOBTree import IOBTree
from persistent.list import PersistentList

from appy.px import Px
from appy import utils
from appy.utils import string as sutils
from appy.model.utils import Object as O
from appy.model.fields import Field, Show
from appy.ui.layout import Layout, Layouts
from appy.model.fields.calendar.views import View
from appy.model.fields.calendar.event import Event
from appy.model.fields.calendar.other import Other
from appy.model.fields.calendar.action import Action
from appy.model.fields.calendar.legend import Legend
from appy.model.fields.calendar.data import EventData
from appy.model.fields.calendar.timeslot import Timeslot
from appy.model.fields.calendar.totals import Total, Totals
from appy.model.fields.calendar.validation import Validation

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
TL_W_EVTS   = 'A multiple calendar has the objective to display a series of ' \
              'other calendars. Its own calendar is disabled: it is useless ' \
              'to define event types for it.'
RENDER_KO   = 'Wrong render mode "%s". Possible render modes are: %s.'
MISS_EN_M   = "When param 'eventTypes' is a method, you must give another " \
              "method in param 'eventNameMethod'."
S_MONTHS_KO = 'Strict months can only be used with timeline calendars.'
ACT_MISS    = 'Action "%s" does not exist or is not visible.'
UNSORT_EVTS = 'Events must be sorted if you want to get spanned events to be ' \
              'grouped.'
EVT_DEL     = '%s deleted (%d)%s.'
EVT_DEL_SL  = '%s deleted at slot %s.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Gradient:
    '''If we need to color the cell of a timeline with a linear gradient,
       this class allows to define the characteristics for this gradient.'''

    def __init__(self, angle='135deg', endColor='transparent'):
        # The angle defining the gradient direction
        self.angle = angle
        # The end color (the start color being defined elsewhere)
        self.endColor = endColor

    def getStyle(self, startColor):
        '''Returns the CSS definition for this gradient'''
        return f'background:linear-gradient({self.angle}, {startColor}, ' \
               f'{self.endColor})'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Layer:
    '''A layer is a set of additional data that can be activated or not on top
       of calendar data. Currently available for timelines only.'''

    def __init__(self, name, label, onCell, activeByDefault=False, legend=None,
                 merge=False):
        # "name" must hold a short name or acronym, unique among all layers
        self.name = name
        # "label" is a i18n label that will be used to produce the layer name in
        # the user interface.
        self.label = label
        # "onCell" must be a method that will be called for every calendar cell
        # and must return a 3-tuple (style, title, content). "style" will be
        # dumped in the "style" attribute of the current calendar cell, "title"
        # in its "title" attribute, while "content" will be shown within the
        # cell. If nothing must be shown at all, None must be returned.
        # This method must accept those args:
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #   date      | the currently walked day (a DateTime instance) ;
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #   other     | the Other instance representing the currently walked
        #             | calendar ;
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #   events    | the list of events (as a list of custom Object instances
        #             | whose attribute "event" points to an instance of class
        #             | appy.model.fields.calendar.event::Event) defined at that
        #             | day in this calendar ;
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # preComputed | the result of Calendar.preCompute (see below).
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.onCell = onCell
        # Is this layer activated by default ?
        self.activeByDefault = activeByDefault
        # "legend" is a method that must produce legend items that are specific
        # to this layer. The method must accept no arg and must return a list of
        # objects (you can use class appy.model.utils.Object) having these
        # attributes:
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #   name   | The legend item name as shown in the calendar ;
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #   style  | The content of the "style" attribute that will be applied
        #          | to the little square ("td" tag) for this item ;
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #  content | The content of this "td" (if any).
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.legend = legend
        # When p_merge is False, if the layer contains info for a given day, the
        # base info will be hidden. Else, it will be merged.
        self.merge = merge
        # Layers will be chained: one layer will access the previous one in the
        # stack via attribute "previous". "previous" fields will automatically
        # be filled by the Calendar.
        self.previous = None

    def getCellInfo(self, o, activeLayers, date, other, events, preComputed):
        '''Get the cell info from this layer or one previous layer when
           relevant.'''
        # Take this layer into account only if active
        if self.name in activeLayers:
            info = self.onCell(o, date, other, events, preComputed)
            if info: return info
        # Get info from the previous layer
        if self.previous:
            return self.previous.getCellInfo(o, activeLayers, date, other,
                                             events, preComputed)

    def getLegendEntries(self, o):
        '''Returns the legend entries by calling method in self.legend'''
        return self.legend(o) if self.legend else None

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Calendar(Field):
    '''This field allows to produce an agenda (monthly view) and view/edit
       events on it.'''

    # Some elements will be traversable
    traverse  = Field.traverse.copy()

    # Required Javascript files
    jsFiles = {'view': ('calendar.js',)}

    # Make some classes available here
    View = View
    Other = Other
    Layer = Layer
    Event = Event
    Total = Total
    Action = Action
    Legend = Legend
    DateTime = DateTime
    Timeslot = Timeslot
    IterSub = utils.IterSub
    Validation = Validation

    traverse['Totals'] = 'perm:read'
    Totals = Totals

    class Layouts(Layouts):
        '''Calendar-specific layouts'''
        b = Layouts(edit='f', view='l-d-f')
        n = Layouts(Layout('l-f', width=None))

        @classmethod
        def getDefault(class_, field):
            '''Default layouts for this Calendar p_field'''
            return class_.n if field.multiple else class_.b

    view = cell = buttons = Px('''
     <div var="view=field.View.get(o, field);
               hook=f'{o.iid}{field.name}';
               timeslots=field.Timeslot.getAll(o, field);
               eventTypes=field.getEventTypes(o);
               allowedEventTypes=field.getAllowedEventTypes(o, eventTypes);
               preComputed=field.getPreComputedInfo(o, view);
               mayEdit=field.mayEdit(o);
               objUrl=o.url;
               others=field.Other.getAll(o, field, preComputed);
               events=field.getAllEvents(o, eventTypes, others);
               allEventTypes, allEventNames=events;
               namesOfDays=field.getNamesOfDays(_);
               showTimeslots=len(timeslots) &gt; 1;
               slotIds=[slot.id for slot in timeslots];
               slotIdsStr=','.join(slotIds);
               mayValidate=field.mayValidate(o);
               activeLayers=field.getActiveLayers(req);
               actions=field.getVisibleActions(o, view.monthDayOne)"
          id=":hook">
      <script>:f'var {field.name}_maxEventLength={field.maxEventLength};'
      </script>
      <script>:field.getAjaxData(hook, o, view, popup=popup,
                                 activeLayers=','.join(activeLayers))</script>

      <!-- Period selector -->
      <div class="controlsP">
       <x>:view.pxPeriodSelector</x>

       <!-- Global actions -->
       <x>:field.Action.px</x>
      </div>

      <!-- The top PX, if defined -->
      <x if="field.topPx">::field.topPx</x>

      <!-- The calendar in itself -->
      <x>:view.px</x>

      <!-- The bottom PX, if defined -->
      <x if="field.bottomPx">::field.bottomPx</x>
     </div>''',

     css='''
      .controlsP { display:flex; margin-bottom:0.3em; gap:0.5em;
                   align-items:center; position:sticky; top:-1.8em;
                   background-color:#f7f8fb }
      .controlsP select { margin:0 }
      .controlsP input[type=checkbox] { margin-right:0.4em }''')

    edit = search = ''

    # Currently supported render modes (see p_render below)
    renderModes = ('month', 'monthMulti', 'dayMulti')

    def __init__(self, eventTypes=None, eventNameMethod=None,
      allowedEventTypes=None, validator=None, default=None, defaultOnEdit=None,
      show=Show.ER_, renderable=None, page='main', group=None, layouts=None,
      move=0, readPermission='read', writePermission='write', width='100%',
      height=300, colspan=1, master=None, masterValue=None, focus=False,
      mapping=None, generateLabel=None, label=None, maxEventLength=50,
      render='month', others=None, timelineName=None, timelineMonthName=None,
      additionalInfo=None, startDate=None, endDate=None, defaultDate=None,
      timeslots=None, colors=None, gradients=None, showUncolored=False,
      columnColors=None, preCompute=None, applicableEvents=None, totalRows=None,
      totalCols=None, validation=None, layers=None, layersSelector=True,
      topPx=None, bottomPx=None, actions=None, selectableEmptyCells=False,
      legend=None, view=None, cell=None, buttons=None, edit=None, editable=True,
      custom=None, xml=None, translations=None, delete=True, beforeDelete=None,
      selectableMonths=6, createEventLabel='which_event', style='calTable',
      strictMonths=False, dayMultiWidth='10em'):
        '''Calendar field constructor'''

        # p_eventTypes can be a "static" list or tuple of strings that identify
        # the types of events that can be stored in this calendar. It can also
        # be a method that computes such a "dynamic" list or tuple. When
        # specifying a static list, an i18n label will be generated for every
        # event type of the list. When specifying a dynamic list, you must also
        # give, in p_eventNameMethod, a method that will accept a single arg
        # (=one of the event types from your dynamic list) and return the "name"
        # of this event as it must be shown to the user.
        self.eventTypes = eventTypes or ()
        self.eventNameMethod = eventNameMethod
        if callable(eventTypes) and not eventNameMethod:
            raise Exception(MISS_EN_M)

        # Among event types, for some users, only a subset of it may be created.
        # "allowedEventTypes" is a method that must accept the list of all
        # event types as single arg and must return the list/tuple of event
        # types that the current user can create.
        self.allowedEventTypes = allowedEventTypes

        # It is not possible to create events that span more days than
        # maxEventLength.
        self.maxEventLength = maxEventLength

        # Various render modes exist. Default is the classical "month" view. The
        # currently proposed renderings are the following. Each value for
        # p_render is a string.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # p_render   | Description
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # month      | [default] Monthly view for an individual calendar
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # monthMulti | Monthly view for a multiple calendar (also called a
        #            | "timeline" view). A multiple calendar collects and
        #            | displays info about individual calendars, each one being
        #            | represented by an instance of class
        #            |
        #            |         appy.model.fields.calendar.other.Other
        #            |
        #            | , via attribute p_others (see below). On a "monthMulti"
        #            | view, on the x axis, we have one column per day, and on
        #            | the y axis, we have one row per individual calendar.
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # dayMulti   | Daily view for a multiple calendar
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.render, self.multiple = self.getRenderInfo(render)

        # It has no sense to define event types in a multiple calendar
        if self.multiple and eventTypes:
            raise Exception(TL_W_EVTS)

        # When displaying a given month for this agenda, one may want to
        # pre-compute, once for the whole month, some information that will then
        # be given as arg for other methods specified in subsequent parameters.
        # This mechanism exists for performance reasons, to avoid recomputing
        # this global information several times. If you specify a method in
        # p_preCompute, it will be called every time a given month is shown, and
        # will receive 2 args: the first day of the currently shown month (as a
        # DateTime object) and the grid of all shown dates (as a result of
        # calling m_getGrid below). This grid may hold a little more than dates
        # of the current month. Subsequently, the return of your method will be
        # given as arg to other methods that you may specify as args of other
        # parameters of this Calendar class (see comments below).
        self.preCompute = preCompute

        # [Multiple only] A method must be specified in parameter p_others. It
        # must accept a single arg (the result of p_self.preCompute) and must
        # return a list of Other objects representing calendars whose events
        # must be shown within this agenda. More precisely, the method can
        # return:
        # - a single Other object;
        # - a list of Other objects;
        # - a list of lists of Other objects, when it has sense to group other
        #   calendars (the month, multiple rendering exploits this).
        self.others = others

        # [Multiple only] A name is shown for every other calendar. If
        # p_timelineName is None (the default), this name will be the title of
        # the object where the other calendar is defined. Else, it will be the
        # result of calling the method specified in p_timelineName. This method
        # must return a string and accepts those args:
        # - other     an Other object;
        # - month     the currently shown month, as a string YYYY/mm
        self.timelineName = timelineName

        # [Month, multiple only] The name of the current month is shown in
        # header in footer rows. If you want to customize this zone, specify a
        # method in the following attribute. It will receive, as args:
        # (1) an object containing infos about the current month, having the
        #     following attributes:
        #     * first: a DateTime object being the first day of the month;
        #     * month: the text representing the current month. The name of the
        #       month may be translated; it may contain XHTML formatting;
        # (2) the calendar's pre-computed data.
        # The method must modify the first arg's "month" attribute.
        self.timelineMonthName = timelineMonthName

        # [Month, individual only] One may want to add, day by day, custom
        # information in the calendar. When a method is given in
        # p_additionalInfo, for every cell of the month view, this method will
        # be called with 2 args: the cell's date and the result of
        # self.preCompute. The method's result (a string that can hold text or
        # a chunk of XHTML) will be inserted in the cell.
        self.additionalInfo = additionalInfo

        # One may limit event encoding and viewing to some period of time,
        # via p_startDate and p_endDate. Those parameters, if given, must hold
        # methods accepting no arg and returning a DateTime object. The
        # start and end dates will then be converted to UTC at 00.00.
        self.startDate = startDate
        self.endDate = endDate

        # If a default date is specified, it must be a method accepting no arg
        # and returning a DateTime object. As soon as the calendar is shown,
        # the period where this date is included will be shown (day, week,
        # month, ... depending on the render mode). If not default date is
        # specified, it will be 'now' at the moment the calendar is shown.
        self.defaultDate = defaultDate

        # p_timeslots are a way to define, within a single day, time ranges. It
        # must be a list of Timeslot objects or a method producing such a list.
        # If you define timeslots, the first one must be the one representing
        # the whole day and must have id "main". Tip: for performance, when
        # defining a method in attribute "timeslots", it is best if you have the
        # possibility, in your app, to pre-compute lists of static timeslots,
        # and if the method you place in attribute "timeslots" simply returns
        # the correct precomputed list (according to some custom condition),
        # instead of creating a dynamic list within this method.
        Timeslot.init(self, timeslots)

        # [Month, multiple only] p_colors must either be a dict of the form
        #
        #                    ~{s_eventType: s_color}~
        #
        # or a method receiving 2 args: an event type and the pre-computed
        # object, and returning an HTML-compliant color for this type (or None
        # if the type must not be colored). Indeed, in a month, multiple
        # calendar, cells are too small to display translated names for event
        # types, so colors are used instead.
        #
        # Tip: the name of a color can be followed by semi-colon-separated CSS
        # properties. For example, if you want to define the dimmed version of
        # some color, the returned color can be: "#d08181;opacity:0.5".
        self.colors = colors

        # [Month, multiple only] When the above-defined attribute p_colors is in
        # use, instead of simply coloring the background of a cell in a timeline
        # with that color, one may define a gradient. It is useful if the
        # event's timeslot doesn't span the whole day: the gradient may
        # represent the "partial" aspect of the timeslot (with, for example, an
        # end color being "transparent"). If you define such gradients in the
        # following attribute, every time a cell will need to be colored, if the
        # timeslot of the corresponding event does not span the whole day, a
        # gradient will be used instead of a plain color. Attribute "gradient"
        # hereafter must hold a dict (or a method returning a dict) whose keys
        # are timeslots (strings) and values are Gradient objects.
        self.gradients = gradients or {}

        # [Month, multiple only] For event types for which p_colors is None,
        # must we still show them ? If yes, they will be represented by a dot
        # with a tooltip containing the event name.
        self.showUncolored = showUncolored

        # [Month, multiple only] In the timeline, the background color for
        # columns can be defined in a method you specify here. This method must
        # accept the current date (as a DateTime object) as unique arg. If None,
        # a default color scheme is used (see appy.model.field.calendar.views.
        # monthMulti.MonthMulti.timelineBgColors). Every time your method
        # returns None, the default color scheme will apply.
        self.columnColors = columnColors

        # [Individual only] For a specific day, all event types may not be
        # applicable. If this is the case, one may specify here a method that
        # defines, for a given day, a sub-set of all event types. This method
        # must accept 3 args:
        #  1. the day in question (as a DateTime object);
        #  2. the list of all event types, which is a copy of the (possibly
        #     computed) p_self.eventTypes;
        #  3. the result of calling p_self.preCompute.
        # The method must modify the 2nd arg and remove, from it, potentially
        # not applicable events. This method can also return a message, that
        # will be shown to the user for explaining him why he can, for this day,
        # only create events of a sub-set of the possible event types (or even
        # no event at all).
        self.applicableEvents = applicableEvents

        # [Month, multiple only] If you want to specify additional rows
        # representing totals, give, in p_totalRows, a list of Totals objects
        # (see appy.model.fields.calendar.totals.Totals) or a method producing
        # such a list.
        monthMulti = self.multiple and self.render == 'month'
        if totalRows and not monthMulti:
            raise Exception(Totals.TOT_KO)
        self.totalRows = totalRows or []

        # Similarly, you can specify additional columns in p_totalCols
        if totalCols and not monthMulti:
            raise Exception(Totals.TOT_KO)
        self.totalCols = totalCols or []

        # A validation process can be associated to a Calendar event. It
        # consists in identifying validators and letting them "convert" event
        # types being wished to final, validated event types. If you want to
        # enable this, define a Validation object (see the hereabove class) in
        # p_validation.
        self.validation = validation

        # [Month, multiple only] p_layers define a stack of layers (as a list or
        # tuple). Every layer must be a Layer object and represents a set of
        # data that can be shown or not on top of calendar data.
        self.layers = self.formatLayers(layers)

        # [Month, multiple only] If p_layersSelector is False, all layers having
        # activeByDefault=True will be shown but the selector allowing to (de)
        # activate layers will not be shown.
        self.layersSelector = layersSelector

        # [Non-multiple only] Beyond permission-based security, p_editable may
        # store a method whose result may prevent the user to edit the calendar
        # field.
        self.editable = editable

        # [Non-multiple only] May the user delete events in this calendar? If
        # p_delete is a method, it must accept an event type as single arg.
        self.delete = delete

        # [Non-multiple only] Before deleting an event, if a method is specified
        # in p_beforeDelete, it will be called with the date and timeslot as
        # args. If the method returns False, the deletion will not occur.
        self.beforeDelete = beforeDelete

        # You may specify PXs that will show specific information, respectively,
        # before and after the calendar.
        self.topPx = topPx
        self.bottomPx = bottomPx

        # p_actions is a list of Action objects allowing to define custom
        # actions to execute based on calendar data.
        self.actions = actions or ()

        # When there is at least one visible action, on a monthly, multiple
        # calendar, timeline cells can be selected: this selection is then given
        # as parameter to the triggered action. If p_selectableEmptyCells is
        # True, all cells are selectable. Else, only cells whose content is not
        # empty are selectable.
        self.selectableEmptyCells = selectableEmptyCells

        # p_legend can hold a Legend object (as an instance of class
        # appy.model.fields.calendar.legend.Legend) that determines legend's
        # characteristcs on a month, multiple calendar.
        self.legend = legend or Legend()

        # [Month, individual only] p_selectableMonths determines the number of
        # months in the past or in the future, relative to the currently shown
        # one, that will be accessible by simply selecting them in a list.
        self.selectableMonths = selectableMonths

        # The i18n label to use when the user creates a new event
        self.createEventLabel = createEventLabel

        # The name of a CSS class for the monthly view table. Several
        # space-separated names can be defined.
        self.style = style

        # [Month, multiple only] If p_strictMonths is True, only days of the
        # current month will be shown. Else, complete weeks will be shown,
        # potentially including some days from the previous and next months.
        if strictMonths and not monthMulti:
            raise Exception(S_MONTHS_KO)
        self.strictMonths = strictMonths

        # Width of a coolumn in the "dayMulti" render mode
        self.dayMultiWidth = dayMultiWidth

        # Call the base constructor

        # p_validator, allowing field-specific validation, behaves differently
        # for the Calendar field. If specified, it must hold a method that will
        # be executed every time a user wants to create an event (or series of
        # events) in the calendar. This method must accept those args:
        #  - date       the date of the event (as a DateTime object);
        #  - eventType  the event type (one among p_eventTypes);
        #  - timeslot   the timeslot for the event (see param p_timeslots) ;
        #  - span       the number of additional days on which the event will
        #               span (will be 0 if the user wants to create an event
        #               for a single day).
        # If validation succeeds (ie, the event creation can take place), the
        # method must return True (boolean). Else, it will be canceled and an
        # error message will be shown. If the method returns False (boolean), it
        # will be a standard error message. If the method returns a string, it
        # will be used as specific error message.
        Field.__init__(self, validator, (0,1), default, defaultOnEdit, show,
          renderable, page, group, layouts, move, False, True, None, None,
          False, None, readPermission, writePermission, width, height, None,
          colspan, master, masterValue, focus, False, mapping, generateLabel,
          label, None, None, None, None, True, False, view, cell, buttons, edit,
          custom, xml, translations)

    def getRenderInfo(self, render):
        '''Extract renderring info from p_render. Raise an error if data is
           incorrect.'''
        # Ensure p_render is among valid values
        modes = Calendar.renderModes
        if render not in modes:
            raise Exception(RENDER_KO % (render, ', '.join(modes)))
        # Extract the "Multi" prefix
        if render.endswith('Multi'):
            r = render[:-5], True
        else:
            r = render, False
        return r

    def formatLayers(self, layers):
        '''Chain layers via attribute "previous"'''
        if not layers: return ()
        i = len(layers) - 1
        while i >= 1:
            layers[i].previous = layers[i-1]
            i -= 1
        return layers

    def log(self, o, msg, date=None):
        '''Logs m_msg, field-specifically prefixed.'''
        prefix = f'{o.iid}:{self.name}'
        if date:
            dateS = date.strftime('%Y/%m/%d')
            prefix = f'{prefix}@{dateS}'
        o.log(f'{prefix}: {msg}')

    def getPreComputedInfo(self, o, view):
        '''Returns the result of calling self.preComputed, or None if no such
           method exists.'''
        pre = self.preCompute
        if pre: return pre(o, view.monthDayOne, view.grid)

    weekDays = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    def getNamesOfDays(self, _):
        '''Returns the translated names of all week days, short and long
           versions.'''
        r = {}
        for day in self.weekDays:
            r[day] = O(name=_(f'day_{day}'), short=_(f'day_{day}_short'))
        return r

    def getColorFor(self, o, eventType, preCompute):
        '''Gets the background color for a cell containing some p_eventType'''
        colors = self.colors
        if colors is None:
            r = None
        elif isinstance(colors, dict):
            r = colors.get(eventType)
        else: # A method
            r = colors(o, eventType, preCompute)
        return r

    def getAdditionalInfoAt(self, o, date, preComputed):
        '''If the user has specified a method in self.additionalInfo, we call
           it for displaying this additional info in the calendar, at some
           p_date.'''
        info = self.additionalInfo
        return info(o, date, preComputed) if info else None

    def getEventTypes(self, o):
        '''Returns the (dynamic or static) event types as defined in
           self.eventTypes.'''
        types = self.eventTypes
        return types(o) if callable(types) else types

    def getAllowedEventTypes(self, o, eventTypes):
        '''Gets the allowed events types for the currently logged user'''
        allowed = self.allowedEventTypes
        return eventTypes if not allowed else allowed(o, eventTypes)

    def getGradients(self, o):
        '''Gets the gradients possibly defined in addition to p_self.colors'''
        gradients = self.gradients
        return gradients(o) if callable(gradients) else gradients

    def dayIsFull(self, date, events, timeslots):
        '''In the calendar full at p_date ? Defined events at this p_date are in
           p_events. We check here if the main timeslot is used or if all
           others are used.'''
        if not events: return
        for e in events:
            if e.timeslot == 'main': return True
        return len(events) == len(timeslots) - 1

    def dateInRange(self, date, view):
        '''Is p_date within the range (possibly) defined for this calendar by
           p_startDate and p_endDate ?'''
        tooEarly = view.startDate and date < view.startDate
        tooLate = view.endDate and not tooEarly and date > view.endDate
        return not tooEarly and not tooLate

    def getApplicableEventTypesAt(self, o, date, eventTypes, preComputed,
                                  forBrowser=False):
        '''Returns the event types that are applicable at a given p_date'''
        # More precisely, it returns an object with 2 attributes:
        # * "events" is the list of applicable event types;
        # * "message", not empty if some event types are not applicable,
        #              contains a message explaining those event types are
        #              not applicable.
        if not eventTypes: return # There may be no event type at all
        if not self.applicableEvents:
            # Keep p_eventTypes as is
            message = None
        else:
            eventTypes = eventTypes[:]
            message = self.applicableEvents(o, date, eventTypes, preComputed)
        r = O(eventTypes=eventTypes, message=message)
        if forBrowser:
            r.eventTypes = ','.join(r.eventTypes)
            if not r.message: r.message = ''
        return r

    def getEventsAt(self, o, date, empty=None):
        '''Returns the list of events that exist at some p_date (=day). p_date
           can be:
           * a DateTime instance;
           * a tuple (i_year, i_month, i_day);
           * a string YYYYmmdd.
        '''
        if self.name not in o.values: return empty
        years = getattr(o, self.name)
        if not years: return empty
        # Get year, month and name from p_date
        if isinstance(date, tuple):
            year, month, day = date
        elif isinstance(date, str):
            year, month, day = int(date[:4]), int(date[4:6]), int(date[6:8])
        else:
            year, month, day = date.year(), date.month(), date.day()
        # Dig into the oobtree
        if year not in years: return empty
        months = years[year]
        if month not in months: return empty
        days = months[month]
        if day not in days: return empty
        return days[day] or empty

    def getEventAt(self, o, date, timeslot='main'):
        '''Get the event defined, for this calendar on this p_o(bject), at this
           p_date and p_timeslot.'''
        events = self.getEventsAt(o, date)
        if not events: return
        for event in events:
            if event.timeslot == timeslot:
                return event

    def getEventTypeAt(self, o, date):
        '''Returns the event type of the first event defined at p_day, or None
           if unspecified.'''
        events = self.getEventsAt(o, date)
        return events[0].eventType if events else None

    def getEventsBySlot(self, o, date, addEmpty=False, ifEmpty='-', expr=None,
                        persist=False):
        '''Returns a list of (s_timeslot, event) tuples for every event defined
           in this calendar on p_o at this p_date.'''
        return Timeslot.getEventsAt(o, self, date, addEmpty, ifEmpty, expr,
                                    persist)

    def standardizeDateRange(self, range):
        '''p_range can have various formats (see m_walkEvents below). This
           method standardizes the date range as a 6-tuple
           (startYear, startMonth, startDay, endYear, endMonth, endDay).'''
        if not range: return
        if isinstance(range, int):
            # p_range represents a year
            return (range, 1, 1, range, 12, 31)
        elif isinstance(range[0], int):
            # p_range represents a month
            year, month = range
            return (year, month, 1, year, month, 31)
        else:
            # p_range is a tuple (start, end) of DateTime instances
            start, end = range
            return (start.year(), start.month(), start.day(),
                    end.year(),   end.month(),   end.day())

    def walkEvents(self, o, callback, dateRange=None):
        '''Walks, on p_o, the calendar value in chronological order for this
           field and calls p_callback for every day containing events. The
           callback must accept 3 args: p_o, the current day (as a DateTime
           instance) and the list of events at that day (the database-stored
           PersistentList instance). If the callback returns True, we stop the
           walk.

           If p_dateRange is specified, it limits the walk to this range. It
           can be:
           * an integer, representing a year;
           * a tuple of integers (year, month) representing a given month
             (first month is numbered 1);
           * a tuple (start, end) of DateTime instances.
        '''
        if self.name not in o.values: return
        yearsDict = getattr(o, self.name)
        if not yearsDict: return
        # Standardize date range
        if dateRange:
            startYear, startMonth, startDay, endYear, endMonth, endDay = \
              self.standardizeDateRange(dateRange)
        # Browse years
        years = list(yearsDict.keys())
        years.sort()
        for year in years:
            # Ignore this year if out of range
            if dateRange:
                if (year < startYear) or (year > endYear): continue
                isStartYear = year == startYear
                isEndYear = year == endYear
            # Browse this year's months
            monthsDict = yearsDict[year]
            if not monthsDict: continue
            months = list(monthsDict.keys())
            months.sort()
            for month in months:
                # Ignore this month if out of range
                if dateRange:
                    if (isStartYear and (month < startMonth)) or \
                       (isEndYear and (month > endMonth)): continue
                    isStartMonth = isStartYear and (month == startMonth)
                    isEndMonth = isEndYear and (month == endMonth)
                # Browse this month's days
                daysDict = monthsDict[month]
                if not daysDict: continue
                days = list(daysDict.keys())
                days.sort()
                for day in days:
                    # Ignore this day if out of range
                    if dateRange:
                        if (isStartMonth and (day < startDay)) or \
                           (isEndMonth and (day > endDay)): continue
                    date = DateTime(f'{year}/{month}/{day} UTC')
                    stop = callback(o, date, daysDict[day])
                    if stop: return

    def getEventsByType(self, o, eventType, minDate=None, maxDate=None,
                        sorted=True, groupSpanned=False):
        '''Returns all the events of a given p_eventType'''
        # If p_eventType is None, it returns events of all types. p_eventType
        # can also be a list or tuple. The return value is a list of 2-tuples
        # whose 1st elem is a DateTime instance and whose 2nd elem is the event.

        # If p_sorted is True, the list is sorted in chronological order. Else,
        # the order is random, but the result is computed faster.

        # If p_minDate and/or p_maxDate is/are specified, it restricts the
        # search interval accordingly.

        # If p_groupSpanned is True, events spanned on several days are grouped
        # into a single event. In this case, tuples in the result are 3-tuples:
        # (DateTime_startDate, DateTime_endDate, event).

        # Prevent wrong combinations of parameters
        if groupSpanned and not sorted:
            raise Exception(UNSORT_EVTS)
        r = []
        if self.name not in o.values: return r
        # Compute "min" and "max" tuples
        if minDate:
            minYear = minDate.year()
            minMonth = (minYear, minDate.month())
            minDay = (minYear, minDate.month(), minDate.day())
        if maxDate:
            maxYear = maxDate.year()
            maxMonth = (maxYear, maxDate.month())
            maxDay = (maxYear, maxDate.month(), maxDate.day())
        # Browse years
        years = getattr(o, self.name)
        for year in years.keys():
            # Don't take this year into account if outside interval
            if minDate and year < minYear: continue
            if maxDate and year > maxYear: continue
            months = years[year]
            # Browse this year's months
            for month in months.keys():
                # Don't take this month into account if outside interval
                thisMonth = (year, month)
                if minDate and thisMonth < minMonth: continue
                if maxDate and thisMonth > maxMonth: continue
                days = months[month]
                # Browse this month's days
                for day in days.keys():
                    # Don't take this day into account if outside interval
                    thisDay = (year, month, day)
                    if minDate and thisDay < minDay: continue
                    if maxDate and thisDay > maxDay: continue
                    events = days[day]
                    # Browse this day's events
                    for event in events:
                        # Filter unwanted events
                        if eventType and not event.matchesType(eventType):
                            continue
                        # We have found a event
                        date = DateTime(f'{year}/{month}/{day} UTC')
                        if groupSpanned:
                            singleRes = [date, None, event]
                        else:
                            singleRes = (date, event)
                        r.append(singleRes)
        # Sort the result if required
        if sorted: r.sort(key=lambda x: x[0])
        # Group events spanned on several days if required
        if groupSpanned:
            # Browse events in reverse order and merge them when appropriate
            i = len(r) - 1
            while i > 0:
                currentDate = r[i][0]
                lastDate = r[i][1]
                previousDate = r[i-1][0]
                currentType = r[i][2].eventType
                previousType = r[i-1][2].eventType
                if (previousDate == (currentDate-1)) and \
                   (previousType == currentType):
                    # A merge is needed
                    del r[i]
                    r[i-1][1] = lastDate or currentDate
                i -= 1
        return r

    def hasEventsAt(self, o, date, events):
        '''Returns True if, at p_date, events are exactly of the same type as
           p_events.'''
        if not events: return
        others = self.getEventsAt(o, date)
        if not others: return
        if len(events) != len(others): return
        i = 0
        while i < len(events):
            if not events[i].sameAs(others[i]): return
            i += 1
        return True

    def getEventName(self, o, eventType):
        '''Gets the name of the event corresponding to p_eventType as it must
           appear to the user.'''
        if self.eventNameMethod:
            return self.eventNameMethod(o, eventType)
        else:
            return o.translate(f'{self.labelId}_event_{eventType}')

    def getAllEvents(self, o, eventTypes, others):
        '''Computes:
           * the list of all event types (from this calendar and p_others);
           * a dict of event names, keyed by event types, for all events
             in this calendar and p_others).'''
        r = [[], {}]
        if eventTypes:
            for et in eventTypes:
                r[0].append(et)
                r[1][et] = self.getEventName(o, et)
        if not others: return r
        for other in utils.IterSub(others):
            eventTypes = other.getEventTypes()
            if eventTypes:
                for et in eventTypes:
                    if et not in r[1]:
                        r[0].append(et)
                        r[1][et] = other.field.getEventName(other.o, et)
        return r

    def getStartDate(self, o):
        '''Get the start date for this calendar if defined'''
        if self.startDate:
            d = self.startDate(o)
            # Return the start date without hour, in UTC
            return DateTime(f'{d.year()}/{d.month()}/{d.day()} UTC')

    def getEndDate(self, o):
        '''Get the end date for this calendar if defined'''
        if self.endDate:
            d = self.endDate(o)
            # Return the end date without hour, in UTC
            return DateTime(f'{d.year()}/{d.month()}/{d.day()} UTC')

    def getDefaultDate(self, o):
        '''Get the default date that must appear as soon as the calendar is
           shown.'''
        default = self.defaultDate
        return default(o) if default else DateTime() # Now

    def mayDelete(self, o, events):
        '''May the user delete p_events ?'''
        delete = self.delete
        if not delete: return
        return delete(o, events[0].eventType) if callable(delete) else True

    def mayEdit(self, o, raiseError=False):
        '''May the user edit calendar events ?'''
        # Check the security-based condition
        if not o.guard.mayEdit(o, self.writePermission, raiseError=raiseError):
            return
        # Check the field-specific condition
        return self.getAttribute(o, 'editable')

    def deleteEvent(self, o, date, timeslot, handleEventSpan=True, log=True,
                    say=True, executeMethods=True):
        '''Deletes an event. If t_timeslot is "*", it deletes all events at
           p_date, be there a single event on the main timeslot or several
           events on other timeslots. Else, it only deletes the event at
           p_timeslot. If p_handleEventSpan is True, req.deleteNext will be used
           to delete successive events, too.'''
        events = self.getEventsAt(o, date)
        if not events: return
        # Execute "beforeDelete"
        if executeMethods and self.beforeDelete:
            r = self.beforeDelete(o, date, timeslot)
            # Abort event deletion when required
            if r is False: return
        daysDict = getattr(o, self.name)[date.year()][date.month()]
        count = len(events)
        eNames = ', '.join([e.getName(o, self, xhtml=False) for e in events])
        if timeslot == '*':
            # Delete all events; delete them also in the following days when
            # relevant.
            del daysDict[date.day()]
            req = o.req
            suffix = ''
            if handleEventSpan and req.deleteNext == 'True':
                nbOfDays = 0
                while True:
                    date = date + 1
                    if self.hasEventsAt(o, date, events):
                        self.deleteEvent(o, date, timeslot, say=False,
                                    handleEventSpan=False, executeMethods=False)
                        nbOfDays += 1
                    else:
                        break
                if nbOfDays: suffix = f', span+{nbOfDays}'
            if handleEventSpan and log:
                msg = EVT_DEL % (eNames, count, suffix)
                self.log(o, msg, date)
        else:
            # Delete the event at p_timeslot
            i = len(events) - 1
            while i >= 0:
                if events[i].timeslot == timeslot:
                    msg = EVT_DEL_SL % (events[i].getName(o, self, xhtml=False),
                                        timeslot)
                    del events[i]
                    if log: self.log(o, msg, date)
                    break
                i -= 1
        if say:
            o.say(o.translate('object_deleted'), fleeting=False)

    def validate(self, o, date, eventType, timeslot, span=0):
        '''The validation process for a calendar is a bit different from the
           standard one, that checks a "complete" request value. Here, we only
           check the validity of some insertion of events within the
           calendar.'''
        if not self.validator: return
        r = self.validator(o, date, eventType, timeslot, span)
        if isinstance(r, str):
            # Validation failed, and we have the error message in "r"
            return r
        # Return a standard message if the validation fails without producing a
        # specific message.
        return r or o.translate('field_invalid')

    traverse['process'] = 'perm:write'
    def process(self, o):
        '''Processes an action coming from the calendar widget, ie, the creation
           or deletion of a calendar event.'''
        # Refined security check
        self.mayEdit(o, raiseError=True)
        req = o.req
        action = req.actionType
        # Get the date and timeslot for this action
        date = DateTime(req.day)
        eventType = req.eventType
        eventSpan = req.eventSpan or 0
        eventSpan = min(int(eventSpan), self.maxEventLength)
        if action == 'createEvent':
            # Trigger validation
            timeslot = req.timeslot or 'main'
            valid = self.validate(o, date, eventType, timeslot, eventSpan)
            if isinstance(valid, str): return valid
            return Event.create(o, self, date, eventType, timeslot=timeslot,
                                eventSpan=eventSpan)
        elif action == 'deleteEvent':
            return self.deleteEvent(o, date, req.timeslot or '*')

    def splitList(self, l, sub): return utils.splitList(l, sub)

    def mayValidate(self, o):
        '''May the currently logged user validate wish events ?'''
        valid = self.validation
        return valid.mayValidate(o) if valid else None

    def getAjaxData(self, hook, o, view, **params):
        '''Initializes an AjaxData object on the DOM node corresponding to
           this calendar field.'''
        # If the calendar is used as mode for a search, carry request keys
        # allowing to identify this search.
        req = o.req
        if req.search:
            parent = ",'searchResults'"
            params['resultMode'] = 'calendar'
        else:
            parent = ''
        # Add the key corresponding to the current period type (month, day,...)
        period = view.periodType
        params[period] = getattr(view, period)
        params['multiple'] = '1' if self.multiple else '0'
        params = sutils.getStringFrom(params)
        return f"new AjaxData('{o.url}/{self.name}/view','POST',{params}," \
               f"'{hook}'{parent})"

    traverse['validateEvents'] = 'perm:write'
    def validateEvents(self, o):
        '''Validate or discard events from the request'''
        return self.validation.do(o, self)

    def getActiveLayers(self, req):
        '''Gets the layers that are currently active'''
        if 'activeLayers' in req:
            # Get them from the request
            layers = req.activeLayers or ()
            r = layers if not layers else layers.split(',')
        else:
            # Get the layers that are active by default
            r = [layer.name for layer in self.layers if layer.activeByDefault]
        return r

    def getVisibleActions(self, o, dayOne):
        '''Return the visible actions among self.actions'''
        r = []
        for action in self.actions:
            show = action.show
            show = show(o, dayOne) if callable(show) else show
            if show: r.append(action)
        return r

    traverse['executeAction'] = 'perm:read'
    def executeAction(self, o):
        '''An action has been triggered from the ui'''
        # Find the action to execute
        req = o.req
        name = req.actionName
        monthDayOne = DateTime(f'{req.month}/01')
        action = None
        for act in self.getVisibleActions(o, monthDayOne):
            if act.name == name:
                action = act
                break
        if not action: raise Exception(ACT_MISS % name)
        # Get the selected cells
        selected = []
        tool = o.tool
        sel = req.selected
        if sel:
            for elems in sel.split(','):
                id, date = elems.split('_')
                # Get the calendar object from "id"
                calendarObj = tool.getObject(id)
                # Get a DateTime instance from "date"
                calendarDate= DateTime(f'{date[:4]}/{date[4:6]}/{date[6:]} UTC')
                selected.append((calendarObj, calendarDate))
        # Execute the action
        return action.action(o, selected, req.comment)

    def getXmlValue(self, o, value):
        '''Not implemented yet'''
        return

    def store(self, o, value):
        '''Stores this complete p_value on p_o'''
        if not self.persist or value is None: return
        # Data can be a IOBTree
        if isinstance(value, IOBTree):
            super().store(o, value)
            return
        # Data can also be a standard dict. It is the case, for example, for
        # calendar data imported from a distant site.
        for year, sub1 in value.items():
            if not sub1: continue
            for month, sub2 in sub1.items():
                if not sub2: continue
                for day, events in sub2.items():
                    if not events: continue
                    date = DateTime(f'{year}/{month}/{day}')
                    for event in events:
                        Event.create(o, self, date, event.eventType,
                                     timeslot=event.timeslot, log=False)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
