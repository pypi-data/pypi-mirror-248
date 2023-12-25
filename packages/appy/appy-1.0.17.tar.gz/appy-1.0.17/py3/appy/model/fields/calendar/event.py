#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from persistent import Persistent
from BTrees.IOBTree import IOBTree
from persistent.list import PersistentList

from appy.model.fields.calendar.data import EventData

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
E_DATA_KO   = 'Object passed in the "data" parameter must be an instance of ' \
              'appy.model.fields.calendar.data.EventData, or a sub-class of it.'
E_MODE_KO   = 'A timeslot or an end date is required. Both are missing.'
E_SPAN_KO   = 'Spreading an event on several days with a eventSpan is only ' \
              'possible when creating an event in a timeslot.'
TSLOT_USED  = 'An event is already defined at this timeslot.'
DAY_FULL    = 'No more place for adding this event.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Factory:
    '''Factory for creating events'''

    def __init__(self, o, field, date, eventType, timeslot='main',
                 eventSpan=None, log=True, deleteFirst=False, end=None,
                 data=None):
        # The object on which calendar data is manipulated
        self.o = o
        # The Calendar field
        self.field = field
        # The day at which the event must be created
        self.date = date
        # The type of the event to create. May come from the request.
        req = o.req
        self.eventType = eventType or req.eventType
        # The timeslot that will host the event, for a slotted event
        self.timeslot = timeslot
        # This will hold the timeslots as defined on p_field, if relevant
        self.timeslots = None
        # Is the event to created "slotted" ?
        self.slotted = timeslot is not None
        # [Slotted events only] The number of subsequent days the event must be
        #                       duplicated on.
        self.eventSpan = eventSpan
        # Must we log the operation ?
        self.log = log
        # Must existing events be deleted prior to creating the new one(s) ?
        self.deleteFirst = deleteFirst
        # [Unslotted events only] The end date and hour, as a DateTime object
        self.end = end
        # Optional custom event data
        self.data = data
        # Get the persistent list of events stored at this p_date on p_o. Create
        # it if it does not exist yet.
        self.events = Event.getList(o, field, date)

    def mergeSlotted(self, events):
        '''If, after adding an event of p_eventType, all timeslots are used with
           events of the same type, we can merge them and create a single event
           of this type in the main timeslot.'''
        # When defining an event in the main timeslot, no merge is needed
        timeslot = self.timeslot
        if timeslot == 'main' or not events: return
        # Merge is required if all events of this p_eventType reach together a
        # part of 1.0.
        count = 0.0
        o = self.o
        field = self.field
        eventType = self.eventType
        timeslots = self.timeslots
        for event in events:
            if event.eventType == eventType:
                count += event.getDayPart(o, field, timeslots)
        Timeslot = field.Timeslot
        if (count + Timeslot.get(timeslot, o, field, timeslots).dayPart) == 1.0:
            # Delete all events of this type and create a single event of this
            # type, with timeslot "main". If custom data was stored on these
            # events, it will be lost.
            i = len(events) - 1
            while i >= 0:
                if events[i].eventType == eventType:
                    del events[i]
                i -= 1
            events.insert(0, Event(eventType, data=self.data))
            return True

    def checkSlotted(self):
        '''Checks if one may create an event of p_self.eventType in this
           p_self.timeslot. Events already defined at the current date are in
           p_self.events. If the creation is not possible, an error message is
           returned.'''
        # The following errors should not occur if we have a normal user behind
        # the ui.
        events = self.events
        timeslot = self.timeslot
        for e in events:
            if e.timeslot == timeslot: return TSLOT_USED
            elif e.timeslot == 'main': return DAY_FULL
        if events and timeslot == 'main': return DAY_FULL
        # Get the Timeslot and check if, at this timeslot, it is allowed to
        # create an event of p_eventType.
        for slot in self.timeslots:
            if slot.id == timeslot:
                # I have the timeslot
                if not slot.allows(self.eventType):
                    _ = self.o.translate
                    return _('timeslot_misfit', mapping={'slot': timeslot})

    def makeSlotted(self, date, events, handleEventSpan):
        '''Create a slotted event in calendar p_self.field. Manage potential
           merging of events and creation of a sequence of events spanned on
           several subsequent days.'''
        # In the case of an event spanned on several subsequent days, when
        # m_makeSlotted will be called recursively for creating the events on
        # these subsequent days, it will be called with p_handleEventSpan being
        # False to avoid infinite recursion.
        timeslot = self.timeslot
        eventType = self.eventType
        event = None
        # Merge this event with others when relevant
        merged = self.mergeSlotted(events)
        if not merged:
            # Create and store the event
            event = Event(eventType, timeslot=timeslot, data=self.data)
            events.append(event)
            # Sort events in the order of timeslots
            if len(events) > 1:
                timeslots = [slot.id for slot in self.timeslots]
                events.sort(key=lambda e: timeslots.index(e.timeslot))
        # Span the event on the successive days if required
        suffix = ''
        eventSpan = self.eventSpan
        if handleEventSpan and eventSpan:
            for i in range(eventSpan):
                nextDate = date + (i+1)
                nextEvents = Event.getList(self.o, self.field, nextDate)
                self.makeSlotted(nextDate, nextEvents, False)
                suffix = f', span+{eventSpan}'
        if handleEventSpan and self.log:
            msg = f'added {eventType}, slot {timeslot}{suffix}'
            self.field.log(self.o, msg, self.date)
        return event

    def makeUnslotted(self):
        '''Create an unslotted event'''
        eventType = self.eventType
        event = Event(eventType, timeslot=None, start=self.date, end=self.end,
                      data=self.data)
        events = self.events
        events.append(event)
        if len(events) > 1:
            # Sort events according to their start date
            events.sort(key=lambda e: e.start)
        if self.log:
            start = self.date
            starT = start.strftime('%H:%M')
            end = self.end
            fmt = '%H:%M' if end.day() == start.day() else '%Y/%m/%d@%H:%M'
            enD = end.strftime(fmt)
            msg = f'added {eventType}, [{starT} → {enD}]'
            self.field.log(self.o, msg, start)
        return event

    def make(self, handleEventSpan=True):
        '''Create an event'''
        # Delete any event if required
        if self.events and self.deleteFirst:
            del self.events[:]
        # Return an error if the creation of a slotted event cannot occur
        if self.slotted:
            self.timeslots = self.field.Timeslot.getAll(self.o, self.field)
            error = self.checkSlotted()
            if error: return error
            # Create a slotted event. Manage potential merging and duplication.
            event = self.makeSlotted(self.date, self.events, handleEventSpan)
        else:
            # Create an unslotted event
            event = self.makeUnslotted()
        # Complete event data, if it exists
        if self.data: self.data.complete(self.o, event)
        if self.log:
            o = self.o
            o.say(o.translate('object_saved'), fleeting=False)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Event(Persistent):
    '''A calendar event as will be stored in the database'''

    def __init__(self, eventType, timeslot='main', start=None, end=None,
                 data=None):
        # The event type, as a string, selected from possible values as defined
        # in attribute Calendar::eventTypes.
        self.eventType = eventType
        # The event timeslot, if the event is "slotted" = if it is to be
        # injected in one of the standard timeslots as defined on the tied
        # Calendar field, in attribute named "timeslots".
        self.timeslot = timeslot
        # The event start and end dates+hours, as DateTime objects, for
        # "unslotted" events defining their own specific schedule.
        self.start = start
        self.end = end
        # Additional, custom data that can be injected in the event, as an
        # instance of class appy.model.fields.calendar.data.EventData, or a
        # custom sub-class.
        self.data = data

    def getName(self, o, field, allEventNames=None, xhtml=True, mode='Month'):
        '''Gets the name for this event, that depends on its type or data and
           may include the timeslot or schedule info.'''
        # The name is based on the event type, excepted when custom data is here
        # and p_xhtml must be rendered. In this latter case, a lot more info can
        # be dumped, and not only a "name".
        data = self.data
        if data and xhtml:
            r, baseData = data.render(o, mode)
        else:
            # If we have the translated names for event types, use it
            r = baseData = None
            if allEventNames:
                if self.eventType in allEventNames:
                    r = allEventNames[self.eventType]
                else:
                    # This can be an old deactivated event not precomputed
                    # anymore in p_allEventNames. Try to use field.getEventName
                    # to compute it.
                    try:
                        r = field.getEventName(o, self.eventType)
                    except Exception:
                        pass
        # If no name was found, use the raw event type
        r = r or self.eventType
        # Define a prefix, based on the start hour or timeslot
        timeslot = self.timeslot
        if timeslot == 'main':
            # No prefix to set: the event spans the entire day
            prefix = ''
        elif timeslot:
            # Add the timeslot as prefix
            prefix = self.timeslot
        else:
            # An unslotted event: add the start hour as prefix
            prefix = self.start.strftime('%H:%M')
        if prefix:
            # Format the prefix and add it to the result
            if xhtml:
                prefix = f'<div class="bottomSpaceXS discreet">{prefix}</div>'
            else:
                prefix = f'{prefix} · '
        # Complete the v_prefix with base data when available
        if baseData: prefix = f'{prefix}{baseData}'
        return f'{prefix}{r}'

    def sameAs(self, other):
        '''Is p_self the same as p_other?'''
        return self.eventType == other.eventType and \
               self.timeslot == other.timeslot

    def getDayPart(self, o, field, timeslots=None):
        '''What is the day part taken by this event ?'''
        id = self.timeslot
        if id == 'main': return 1.0
        # Get the dayPart attribute as defined on the Timeslot object
        return field.Timeslot.get(self.timeslot, o, field, timeslots).dayPart

    def getTimeMark(self):
        '''Returns short info about the event time: the timeslot for a slotted
           event, or the start date else.'''
        return self.timeslot or self.start.strftime('%H:%M')

    def matchesType(self, type):
        '''Is p_self an event of this p_type ?'''
        # p_type can be:
        # - a single event type (as a string),
        # - a prefix denoting several event types (as a string ending with a *),
        # - a list of (unstarred) event types.
        etype = self.eventType
        if isinstance(type, str):
            if type.endswith('*'):
                r = etype.startswith(type[:-1])
            else:
                r = etype == type
        else:
            r = etype in type
        return r

    def __repr__(self):
        '''p_self's short string representation'''
        if self.timeslot:
            suffix = f'@slot {self.timeslot}'
        else:
            suffix = f'@{self.start.strftime("%H:%M")}'
        return f'‹Event {self.eventType} {suffix}›'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                    Class methods for creating an event
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @classmethod
    def getList(class_, o, field, date):
        '''Gets the persistent list of events defined on this p_o(bject) for
           this calendar p_field at thid p_date. If it does not exist, it is
           created.'''
        # Split the p_date into separate parts
        year, month, day = date.year(), date.month(), date.day()
        # Create, on p_o, the calendar data structure if it doesn't exist yet
        name = field.name
        yearsDict = o.values.get(name)
        if yearsDict is None:
            # 1st level: create a IOBTree whose keys are years
            yearsDict = IOBTree()
            setattr(o, name, yearsDict)
        # Get the sub-dict storing months for a given year
        if year in yearsDict:
            monthsDict = yearsDict[year]
        else:
            yearsDict[year] = monthsDict = IOBTree()
        # Get the sub-dict storing days of a given month
        if month in monthsDict:
            daysDict = monthsDict[month]
        else:
            monthsDict[month] = daysDict = IOBTree()
        # Get the list of events for a given day
        if day in daysDict:
            events = daysDict[day]
        else:
            daysDict[day] = events = PersistentList()
        return events

    @classmethod
    def create(class_, o, field, date, eventType, timeslot='main',
               eventSpan=None, log=True, deleteFirst=False, end=None,
               data=None):
        '''Create a new event of some p_eventType in this calendar p_field on
           p_o, at some p_date (day), being a DateTime object.'''

        # 2 different kinds of events can be created: events to "inject" in some
        # predefined p_timeslot, or "free-style" events, defining their own
        # specific schedule (start and end date/hour).

        # For creating an event in a timeslot, the p_timeslot identifier must be
        # defined. In that mode only, if an p_eventSpan is defined, the same
        # event will be duplicated in the p_eventSpan days following p_date.

        # For creating an own-scheduled event, set p_timeslot to None. p_date
        # must hold the event's own start date and hour; p_end must be passed
        # and hold the event's end date and hour, as a hour-aware DateTime
        # object.

        # In any mode, if p_deleteFirst is True, any existing event found at
        # p_date will be deleted before creating the new event.

        # In any mode, a custom EventData object can be passed in p_data. When
        # creating multiple events due to p_eventSpan, p_data is only associated
        # to the first created event.

        # Ensure parameters' correctness
        slotted = end is None
        if timeslot is None and slotted:
            raise Exception(E_MODE_KO)
        if not slotted and eventSpan is not None:
            raise Exception(E_SPAN_KO)
        if data is not None and not isinstance(data, EventData):
            raise Exception(E_DATA_KO)

        # Delegate the event creation to a factory
        factory = Factory(o, field, date, eventType, timeslot, eventSpan, log,
                          deleteFirst, end, data)
        return factory.make(handleEventSpan=True)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
