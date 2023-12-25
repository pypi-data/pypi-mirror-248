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
from DateTime import DateTime

from appy.px import Px
from appy.utils import dates as dutils
from appy.model.utils import Object as O
from appy.model.fields.calendar.views import View

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Month(View):
    '''Represents a calendar, monthly view for an individual calendar'''

    # Default month format
    periodFormat = '%Y/%m'

    def __init__(self, o, field):
        # Call the base constructor
        super().__init__(o, field)
        # Determine the month to show
        self.month = self.req.month or self.defaultDateS
        # What is the first day of the month ?
        self.monthDayOne = DateTime(f'{self.month}/01')
        # Set the grid
        self.grid = self.getGrid()
        # Get the surrounding months
        self.around = self.getSurrounding()

    def getInfo(self, first):
        '''Returns an Object instance representing information about the month
           having this day as p_first day (DateTime object).'''
        text = self.tool.formatDate(first, '%MT %Y', withHour=False)
        return O(id=first.strftime('%Y/%m'), text=text)

    def getGrid(self, period=None):
        '''Creates a list of DateTime objects representing the calendar grid to
           render for the current p_self.month, or the month specified in
           p_period if passed. If p_self is a Month object, it is a list of
           lists (one sub-list for every week; indeed, every week is rendered as
           a row). If p_self is a MonthMulti object, the result is a linear list
           of DateTime objects.'''
        # Month is a string "YYYY/mm"
        month = period or self.month
        currentDay = DateTime(f'{month}/01 UTC')
        currentMonth = currentDay.month()
        isLinear = self.multiple
        r = [] if isLinear else [[]]
        dayOneNb = currentDay.dow() or 7 # This way, Sunday is 7 and not 0
        strictMonths = self.field.strictMonths
        if dayOneNb != 1 and not strictMonths:
            # If I write "previousDate = DateTime(currentDay)", the date is
            # converted from UTC to GMT
            previousDate = DateTime(f'{month}/01 UTC')
            # If the 1st day of the month is not a Monday, integrate the last
            # days of the previous month.
            for i in range(1, dayOneNb):
                previousDate -= 1
                target = r if isLinear else r[0]
                target.insert(0, previousDate)
        finished = False
        while not finished:
            # Insert currentDay in the result
            if isLinear:
                r.append(currentDay)
            else:
                if len(r[-1]) == 7:
                    # Create a new row
                    r.append([currentDay])
                else:
                    r[-1].append(currentDay)
            currentDay += 1
            if currentDay.month() != currentMonth:
                finished = True
        # Complete, if needed, the last row with the first days of the next
        # month. Indeed, we may need to have a complete week, ending with a
        # Sunday.
        if not strictMonths:
            target = r if isLinear else r[-1]
            while target[-1].dow() != 0:
                target.append(currentDay)
                currentDay += 1
        return r

    def getSurrounding(self):
        '''Gets the months surrounding the current one'''
        first = self.monthDayOne
        r = O(next=None, previous=None, all=[self.getInfo(first)])
        # Calibrate p_startDate and p_endDate to the first and last days of
        # their month. Indeed, we are interested in months, not days, but we use
        # arithmetic on days.
        start = self.startDate
        if start: start = DateTime(start.strftime('%Y/%m/01 UTC'))
        end = self.endDate
        if end: end = dutils.getLastDayOfMonth(end)
        # Get the x months after p_first
        mfirst = first
        i = 1
        selectable = self.field.selectableMonths
        while i <= selectable:
            # Get the first day of the next month
            mfirst = DateTime((mfirst + 33).strftime('%Y/%m/01 UTC'))
            # Stop if we are above self.endDate
            if end and mfirst > end:
                break
            info = self.getInfo(mfirst)
            r.all.append(info)
            if i == 1:
                r.next = info
            i += 1
        # Get the x months before p_first
        mfirst = first
        i = 1
        while i <= selectable:
            # Get the first day of the previous month
            mfirst = DateTime((mfirst - 2).strftime('%Y/%m/01 UTC'))
            # Stop if we are below self.startDate
            if start and mfirst < start:
                break
            info = self.getInfo(mfirst)
            r.all.insert(0, info)
            if i == 1:
                r.previous = info
            i += 1
        return r

    def getCellClass(self, date):
        '''What CSS class(es) must apply to the table cell representing p_date
           in the calendar?'''
        r = []
        # We must distinguish between past and future dates
        r.append('odd' if date < self.today else 'even')
        # Week-end days must have a specific style
        if date.aDay() in ('Sat', 'Sun'): r.append('cellWE')
        return ' '.join(r)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                                  PXs
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Month selector
    pxPeriodSelector = Px('''
     <div var="fmt='%Y/%m/%d';
               around=view.around;
               goBack=not view.startDate or around.previous;
               goForward=not view.endDate or around.next">

      <!-- Go to the previous month -->
      <img class="clickable iconS" if="goBack"
           var2="prev=around.previous" title=":prev.text"
           src=":svg('arrow')" style="transform:rotate(90deg)"
           onclick=":'askMonth(%s,%s)' % (q(hook), q(prev.id))"/>

      <!-- Go back to the default date -->
      <input type="button" if="goBack or goForward"
        var2="fmt='%Y/%m';
             sdef=view.defaultDate.strftime(fmt);
            disabled=sdef == view.monthDayOne.strftime(fmt);
           label='today' if sdef == view.today.strftime(fmt) else 'goto_source'"
        value=":_(label)" disabled=":disabled"
        style=":'color:%s' % ('grey' if disabled else 'black')"
        onclick=":'askMonth(%s,%s)' % (q(hook), q(view.defaultDateS))"/>

      <!-- Display the current month and allow to select another one -->
      <select id="monthChooser" onchange=":f'askMonth({q(hook)}, this.value)'">
       <option for="m in around.all" value=":m.id"
               selected=":m.id == view.month">:m.text</option>
      </select>

      <!-- Go to the next month -->
      <img if="goForward" class="clickable iconS" 
           var2="next=around.next" title=":next.text" src=":svg('arrow')"
           style="transform:rotate(270deg)"
           onclick=":'askMonth(%s,%s)' % (q(hook), q(next.id))"/>
     </div>''')

    # Popup for adding an event in the month view
    pxAddPopup = Px('''
     <div var="popupId=f'{hook}_new';
               submitJs='triggerCalendarEvent(%s, %s, %s_maxEventLength)' % \
                        (q(hook), q('new'), field.name)"
          id=":popupId" class="popup" align="center">
      <form id=":f'{popupId}Form'" method="post" data-sub="process">
       <input type="hidden" name="actionType" value="createEvent"/>
       <input type="hidden" name="day"/>

       <!-- Choose an event type -->
       <div align="center">:_(field.createEventLabel)</div>
       <select name="eventType" class="calSelect">
        <option value="">:_('choose_a_value')</option>
        <option for="eventType in allowedEventTypes"
                value=":eventType">:allEventNames[eventType]</option>
       </select>

       <!-- Choose a timeslot -->
       <div if="showTimeslots">
        <span class="discreet">:_('timeslot')</span> 
        <select if="showTimeslots" name="timeslot" class="calSelect">
         <option for="sname, slot in field.Timeslot.getAllNamed(o, timeslots)"
                 value=":slot.id">:sname</option>
        </select>
       </div>

       <!-- Span the event on several days -->
       <div align="center" class="calSpan">
        <x>::_('event_span')</x>
        <input type="text" size="1" name="eventSpan"
               onkeypress="return (event.keyCode != 13)"/>
       </div>
       <input type="button" value=":_('object_save')" onclick=":submitJs"/>
       <input type="button" value=":_('object_cancel')"
              onclick=":f'closePopup({q(popupId)})'"/>
      </form>
     </div>''',

     css='''.calSelect { margin:10px 0; color:|selectColor|; font-size:95% }
            .calSpan { margin-bottom:3px; font-size:92%; color:|selectColor| }
            .calSpan input { color:|selectColor|; text-align:center }
     ''')

    # Popup for removing events in the month view
    pxDelPopup = Px('''
     <div var="popupId=f'{hook}_del'"
          id=":popupId" class="popup" align="center">
      <form id=":f'{popupId}Form'" method="post" data-sub="process">
       <input type="hidden" name="actionType" value="deleteEvent"/>
       <input type="hidden" name="timeslot" value="*"/>
       <input type="hidden" name="day"/>
       <div align="center"
            style="margin-bottom: 5px">:_('action_confirm')</div>

       <!-- Delete successive events ? -->
       <div class="discreet" style="margin-bottom:10px"
            id=":f'{hook}_DelNextEvent'"
            var="cbId=f'{popupId}_cb'; hdId=f'{popupId}_hd'">
         <input type="checkbox" name="deleteNext_cb" id=":cbId"
                onClick="toggleCheckbox(this)"/><input
          type="hidden" id=":hdId" name="deleteNext"/>
         <label lfor=":cbId" class="simpleLabel">:_('del_next_events')</label>
       </div>
       <input type="button" value=":_('yes')"
              onClick=":'triggerCalendarEvent(%s, %s)' % (q(hook), q('del'))"/>
       <input type="button" value=":_('no')"
              onclick=":f'closePopup({q(popupId)})'"/>
      </form>
     </div>''')

    # Main PX
    px = Px('''
     <table cellpadding="0" cellspacing="0" width=":field.width"
            class=":field.style" id=":f'{hook}_cal'"
            var="rowHeight=int(field.height/float(len(view.grid)))">

      <!-- 1st row: names of days -->
      <tr height="22px">
       <th for="dayId in field.weekDays"
           width="14%">:namesOfDays[dayId].short</th>
      </tr>

      <!-- The calendar in itself -->
      <tr for="row in view.grid" valign="top" height=":rowHeight">
       <x for="date in row"
          var2="inRange=field.dateInRange(date, view);
                cssClasses=view.getCellClass(date)">
        <!-- Dump an empty cell if we are out of the supported date range -->
        <td if="not inRange" class=":cssClasses"></td>
        <!-- Dump a normal cell if we are in range -->
        <td if="inRange"
            var2="events=field.getEventsAt(o, date);
                  single=events and len(events) == 1;
                  spansDays=field.hasEventsAt(o, date+1, events);
                  mayCreate=mayEdit and not field.dayIsFull(date, events,
                                                            timeslots);
                  mayDelete=mayEdit and events and field.mayDelete(o, events);
                  day=date.day();
                  dayString=date.strftime('%Y/%m/%d');
                  js='itoggle(this)' if mayEdit else ''"
            style=":'font-weight:%s' % \
                    ('bold' if date.isCurrentDay() else 'normal')"
            class=":cssClasses" onmouseover=":js" onmouseout=":js">
         <span>:day</span> 
         <span if="day == 1">:_(f'month_{date.aMonth()}_short')</span>
         <!-- Icon for adding an event -->
         <x if="mayCreate">
          <img class="clickable" style="visibility:hidden"
               var="info=field.getApplicableEventTypesAt(o, date, \
                          eventTypes, preComputed, True)"
               if="info and info.eventTypes" src=":url('plus')"
               var2="freeSlots=field.Timeslot.getFreeAt(date, events, slotIds,
                                                        slotIdsStr, True)"
               onclick=":'openEventPopup(%s,%s,%s,null,null,%s,%s,%s)' % \
                (q(hook), q('new'), q(dayString), q(info.eventTypes), \
                 q(info.message), q(freeSlots))"/>
         </x>
         <!-- Icon for deleting event(s) -->
         <img if="mayDelete" class="clickable iconS" style="visibility:hidden"
              src=":svg('deleteS' if single else 'deleteMany')"
              onclick=":'openEventPopup(%s,%s,%s,%s,%s)' %  (q(hook), \
                         q('del'), q(dayString), q('*'), q(spansDays))"/>
         <!-- Events -->
         <x if="events">
         <div for="event in events" style="color:grey">
          <!-- Checkbox for validating the event -->
          <input type="checkbox" checked="checked" class="smallbox"
              if="mayValidate and field.validation.isWish(o, event.eventType)"
              id=":'%s_%s_%s' % (date.strftime('%Y%m%d'), event.eventType, \
                                 event.getTimeMark())"
              onclick=":f'onCheckCbCell(this,{q(hook)})'"/>
          <x>::event.getName(o, field, allEventNames)</x>
          <!-- Icon for delete this particular event -->
           <img if="mayDelete and not single" class="clickable iconS"
                src=":svg('deleteS')"  style="visibility:hidden"
                onclick=":'openEventPopup(%s,%s,%s,%s)' % (q(hook), \
                           q('del'), q(dayString), q(event.timeslot))"/>
         </div>
         </x>
         <!-- Events from other calendars -->
         <x if="others"
            var2="otherEvents=field.Other.getEventsAt(field, date, others,
                                             allEventNames, view, preComputed)">
          <div style=":f'color:{event.color}; font-style:italic'"
               for="event in otherEvents">:event.name</div>
         </x>
         <!-- Additional info -->
         <x var="info=field.getAdditionalInfoAt(o, date, preComputed)"
            if="info">::info</x>
        </td>
       </x>
      </tr>
     </table>

     <!-- Popups for creating and deleting a calendar event -->
     <x if="mayEdit and eventTypes">
      <x>:view.pxAddPopup</x><x>:view.pxDelPopup</x></x>''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
