import collections

from . import shortcuts

from ..concentrations.fixed_concentration import ZeroConcentration

def make_concentrations(parameter_value_map, concentrations):
    result = collections.defaultdict(ZeroConcentration)
    for conc in concentrations:
        result[conc.state] = shortcuts.make_concentration(parameter_value_map,
                                                          conc)
    return result
