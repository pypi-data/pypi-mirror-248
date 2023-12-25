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
from appy.px import Px
from appy.model.fields.calendar.views.day import Day

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class DayMulti(Day):
    '''Represents a calendar, daily view for several individual calendars'''

    multiple = True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                                  PXs
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def getColumnWidth(self, cal):
        '''Returns the width and min-width properties for every column'''
        return f'width:{cal.dayMultiWidth};min-width:{cal.dayMultiWidth}'

    # Main PX
    px = Px('''
     <table width="100%" class="dayMulti">
      <!-- First row: sub-calendar names -->
      <thead>
       <tr>
        <th></th>
        <x for="groupO in others">
         <th for="other in groupO" style=":view.getColumnWidth(field)">
          <b>::view.getNameOnMulti(other)</b>
         </th>
        </x>
        <th></th>
       </tr>
      </thead>
      <!-- Next rows: one row per hour of the day -->
      <tbody>
       <tr for="i in range(24)" var2="hour=f'{str(i).zfill(2)}:00'"
           id=":f'h{i}'" class=":'current' if view.now.hour()==i else ''">
        <td>:hour</td>
         <x for="groupO in others">
          <td for="other in groupO"
              var2="allEvents=view.getEventsPerHour(other);
                    events=allEvents.get(i)">
           <x for="event in (events or())">::view.renderEvent(event, other.o,
                                                         other.field, _ctx_)</x>
          </td>
         </x>
        <td>:hour</td>
       </tr>
      </tbody>
     </table>
     <script>::view.scrollToHour()</script>''',

     css='''
     .dayMulti td, .dayMulti th { padding:0.2em 0.6em }
     .dayMulti>thead>tr:first-child { background-color:#f7f8fb;
                                      position:sticky; top:0.6em }
     .dayMulti>tbody>tr { vertical-align:top }
     .dayMulti>tbody>tr>td:not(:last-child) { border-right:1px solid grey }
     .dayMulti>tbody>tr:not(:last-child)>td {
       border-bottom:1px solid lightgrey }
     .dayMulti .current { background-color:#eeeeee}''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
