#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from appy.px import Px

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Sidebar:
    '''The Appy sidebar'''

    def __init__(self, width='320px', minWidth=None):
        '''Create a Sidebar object on a Appy class, in static attribute named
           "sidebar", if you want to display a sidebar for objects of this
           class.'''
        self.width = width
        self.minWidth = minWidth or width

    @classmethod
    def get(class_, tool, o, layout, popup):
        '''The sidebar must be shown when p_o declares to use the sidebar. If
           it must be shown, its width is returned.'''
        if not o or popup: return
        sidebar = getattr(o.class_.python, 'sidebar', None)
        if not sidebar: return
        if callable(sidebar): sidebar = sidebar(o, layout)
        return sidebar

    def getStyle(self, collapse):
        '''Gets the CSS properties to apply to the sidebar'''
        return f'{collapse.style};width:{self.width};min-width:{self.minWidth}'

    px = Px('''
     <div var="page,grouped,css,js,phases=o.getGroupedFields('main','sidebar');
               collapse=ui.Collapsible.get('sidebar', dright, req)"
          id=":collapse.id" class="sidebar"
          style=":sidebar.getStyle(collapse)">
      <x>::ui.Includer.getSpecific(tool, css, js)</x>
      <x var="layout='view'">:o.pxFields</x>
     </div>''',

     css='''.sidebar { padding:|sbPadding|; position:sticky; top:0;
                       overflow-y:auto; overflow-x:auto }''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
