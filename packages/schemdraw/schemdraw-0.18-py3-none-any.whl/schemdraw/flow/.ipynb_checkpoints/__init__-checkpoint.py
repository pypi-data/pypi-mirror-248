from .flow import Box, RoundBox, Subroutine, Data, Start, Ellipse, Decision, Connect, Process, RoundProcess
from .flow import Terminal, Circle, State, StateEnd
from ..elements import Arrow, Arrowhead, Line, Dot, Wire, Arc2, Arc3, ArcZ, ArcN, ArcLoop

__all__ = ['Box', 'RoundBox', 'Subroutine', 'Data', 'Start', 'Ellipse', 'Decision', 'Connect',
           'Process', 'RoundProcess', 'Terminal', 'Circle', 'State', 'StateEnd', 'Arrow',
           'Arrowhead', 'Line', 'Dot', 'Wire', 'Arc2', 'Arc3', 'ArcZ', 'ArcN', 'ArcLoop']


def style(style):
    ''' Set global element style

        Args:
            style: dictionary of elementname: Element
            to change the element module namespace.
            Use `elements.STYLE_IEEE` or `elements.STYLE_IEC`
            to define U.S./IEEE or European/IEC element styles.
    '''
    for name, element in style.items():
        globals()[name] = element