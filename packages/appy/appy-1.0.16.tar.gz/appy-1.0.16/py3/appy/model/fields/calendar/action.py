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

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Action:
    '''An action represents a custom method that can be executed, based on
       calendar data. If at least one action is visible, the shown calendar
       cells will become selectable: the selected cells will be available to the
       action.'''

    # Currently, actions can be defined in month, multiple calendars only

    def __init__(self, name, label, action, show=True, valid=None):
        # A short name that must identify this action among all actions defined
        # in this calendar.
        self.name = name
        # "label" is a i18n label that will be used to name the action in the
        # user interface.
        self.label = label
        # "labelConfirm" is the i18n label used in the confirmation popup. It
        # is based on self.label, suffixed with "_confirm".
        self.labelConfirm = f'{label}_confirm'
        # "action" is the method that will be executed when the action is
        # triggered. It accepts 2 args:
        # - "selected": a list of tuples (obj, date). Every such tuple
        #               identifies a selected cell: "obj" is the object behind
        #               the "other" calendar into which the cell is; "date" is a
        #               DateTime instance that represents the date selected in
        #               this calendar.
        #               The list can be empty if no cell has been selected.
        # - "comment"  the comment entered by the user in the confirm popup.
        self.action = action
        # Must this action be shown or not? "show" can be a boolean or a method.
        # If it is a method, it must accept a unique arg: a DateTime instance
        # being the first day of the currently shown month.
        self.show = show
        # Is the combination of selected events valid for triggering the action?
        self.valid = None

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #                                  PXs
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # The range of widgets (checkboxes, buttons) allowing to trigger actions
    px = Px('''
     <x>
      <!-- Validate button, with checkbox for automatic checbox selection -->
      <x if="mayValidate" var2="cbId=f'{hook}_auto'">
       <input if="mayValidate" type="button" value=":_('validate_events')"
              class="buttonSmall button" style=":url('validate', bg=True)"
              var2="js='validateEvents(%s,%s)' % (q(hook), q(view.month))"
              onclick=":'askConfirm(%s,%s,%s)' % (q('script'), q(js, False),
                        q(_('validate_events_confirm')))"/>
       <input type="checkbox" checked="checked" id=":cbId"/>
       <label lfor=":cbId" class="simpleLabel">:_('select_auto')</label>
      </x>

      <!-- Checkboxes for (de-)activating layers -->
      <x if="field.layers and field.layersSelector">
       <x for="layer in field.layers"
          var2="cbId=f'{hook}_layer_{layer.name}'">
        <input type="checkbox" id=":cbId" checked=":layer.name in activeLayers"
               onclick=":f'switchCalendarLayer({q(hook)},this)'"/>
        <label lfor=":cbId" class="simpleLabel">:_(layer.label)</label>
       </x>
      </x>

      <!-- Custom actions -->
      <x if="actions">
       <input for="action in actions" type="button" value=":_(action.label)"
              var2="js='calendarAction(%s,%s,comment)' %
                        (q(hook), q(action.name))"
              onclick=":'askConfirm(%s,%s,%s,true)' % (q('script'),
                         q(js,False), q(_(action.labelConfirm)))"/>

       <!-- Icon for unselecting all cells -->
       <img src=":url('unselect')" title=":_('unselect_all')" class="clickable"
           onclick=":f'calendarUnselect({q(hook)})'"/>
      </x>
     </x>''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
