'''Views for a calendar'''

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

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class View:
    '''Abstract class representing any calendar view, be it individual or
       multiple, whatever period type: monthly, weekly, daily.'''

    # Among all views, one may distinguish individual views, containing info
    # about a single individual or object, from multiple views, showing info
    # about several individual views.
    multiple = False

    def __init__(self, o, field):
        '''View constructor'''
        self.o = o
        self.req = o.req
        self.tool = o.tool
        self.field = field
        # Compute the period type
        self.periodType = self.getPeriodType()
        # The default date to show (+ its string representation)
        self.defaultDate = field.getDefaultDate(o)
        self.defaultDateS = self.defaultDate.strftime(self.periodFormat)
        # Today
        self.today = DateTime('00:00')
        self.now = DateTime() # With the precise hour and minute
        # The time period covered by the calendar may be restricted
        self.startDate = field.getStartDate(o)
        self.endDate = field.getEndDate(o)

    def getPeriodType(self):
        '''Gets the period type as manipulated by this view (month, day...)'''
        r = self.__class__.__name__.lower()
        if r.endswith('multi'):
            r = r[:-5]
        return r

    def getGrid(self, period=None):
        '''Returns the list of DateTime objects (one per day) corresponding to
           the period of time being shown at a time in the view, or to p_period
           if passed.'''
        # Must be called by child classes, within their overridden constructor.
        # The grid must be placed in attribute named p_self.grid.

    def getNameOnMulti(self, other):
        '''Returns the name of some p_other calendar as must be shown in a
           multiple view.'''
        method = self.field.timelineName
        period = self.req[self.periodType] or self.defaultDateS
        if method:
            r = method(self.o, other, period, self.grid)
        else:
            r = f'<a href="{other.o.url}?{self.periodType}={period}">' \
                f'{other.o.getShownValue()}</a>'
        return r

    def renderEvent(self, event, o, field, c):
        '''Returns a representation for p_event on p_self'''
        # The name of the render class is passed: the event may be rendered
        # differently according to it.
        className = self.__class__.__name__
        return event.getName(o, field, c.allEventNames, mode=className)

    @classmethod
    def get(class_, o, field):
        '''Return a concrete View object for viewing this calendar p_field on
           this p_object.'''
        # Deduce the name of the concrete class from p_field rendering-related
        # attributes.
        suffix = 'Multi' if field.multiple else ''
        render = field.render
        className = f'{render.capitalize()}{suffix}'
        moduleName = f'{render}{suffix}'
        exec(f'from appy.model.fields.calendar.views.{moduleName} ' \
             f'import {className}')
        concrete = eval(className)
        return concrete(o, field)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
