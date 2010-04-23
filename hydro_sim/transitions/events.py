from collections import namedtuple

__all__ = ['depolymerization', 'polymerization', 'hydrolysis']

depolymerization = namedtuple('depolymerization', 'end', 'state')
polymerization   = namedtuple('polymerization',   'end', 'state')

hydrolysis = namedtuple('hydrolysis', 'old_state', 'new_state', 'position')

del namedtuple
