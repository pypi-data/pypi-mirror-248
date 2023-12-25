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
from appy.model.fields.calendar.views import View

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Day(View):
    '''Represents a calendar, individual daily view'''

    # Default day format (the one in use in the HTML input[type=date] widget)
    periodFormat = '%Y-%m-%d'

    def __init__(self, o, field):
        # Call the base constructor
        super().__init__(o, field)
        # Determine the day to show
        day = self.req.day
        if day:
            self.day = day
            self.dayO = DateTime(day)
        else:
            self.dayO = self.defaultDate
            self.day = self.dayO.strftime(self.periodFormat)
        # The first day of the month must be defined, in order to conform to the
        # View API.
        month = self.dayO.strftime('%Y/%m')
        self.monthDayOne = DateTime(f'{month}/01')
        # Define the grid
        self.grid = self.getGrid()

    def getGrid(self, period=None):
        '''The grid, for a daily view, only contains the day in question'''
        day = DateTime(period) if period else self.dayO
        return [day]

    def getEventsPerHour(self, other=None):
        '''Returns a dict containing all events occurring at p_self.day, in
           calendar p_self.field or (an)p_other one if passed.'''
        # Within this dict, keys are the hours into which the event's start hour
        # is included.
        #
        # For example, if event A starts at 9:15, B at 9:55 and C at 23:06, the
        # dict will be {9: [A, B], 23: C}.
        #
        # Any event having a timeslot for which no hour range is defined, will
        # be added in a list at key None.
        if other:
            cal = other.field
            o = other.o
        else:
            cal = self.field
            o = self.o
        # The info can be cached
        cache = o.cache
        key = f'{o.iid}{cal.name}'
        if key in cache: return cache[key]
        # Walk all events at self.day
        r = {}
        for event in cal.getEventsAt(o, self.dayO, empty=()):
            start = event.start # Can be None
            if start:
                start = start.hour()
            if start in r:
                r[start].append(event)
            else:
                r[start] = [event]
        # Cache and return the result
        cache[key] = r
        return r

    def scrollToHour(self):
        '''Produce the JJS code alowing to scroll to the current hour within a
           daily view.'''
        return f'document.getElementById("h{self.now.hour()}").' \
               f'scrollIntoView(false)'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                                  PXs
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Day selector

    # The day selector
    pxPeriodSelector = Px('''
     <div class="daySel" var="js='askAjax(%s,null,{%%s:%%s})' % q(hook)">

      <!-- Go to the previous day -->
      <img class="clickable iconS" src=":svg('arrow')"
           style="transform:rotate(90deg)"
           var="prevDay=(view.dayO-1).strftime(view.periodFormat)"
           onclick=":js % (q('day'), q(prevDay))"/>

      <!-- The current day, in a date widget -->
      <div>:tool.formatDate(view.dayO, format="%DT", withHour=False)</div>
      <input type="date" value=":view.day"
             onchange=":js % (q('day'), 'this.value')"/>

      <!-- Go to the next day -->
      <img class="clickable iconS" src=":svg('arrow')"
           style="transform:rotate(270deg)"
           var="nextDay=(view.dayO+1).strftime(view.periodFormat)"
           onclick=":js % (q('day'), q(nextDay))"/>
     </div>''',

     css='''
      .daySel { display:flex; align-items:center; padding:0.5em; width:100%;
                background-color:#f7f8fb; opacity:0.92 }
      .daySel input[type=date] { margin-left:0.4em; width:7.5em }''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
