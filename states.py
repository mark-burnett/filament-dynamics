# Monomer chemical state enumeration
class ChemicalState(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return "<ChemicalState: %s>" % self

ChemicalState.ATP   = ChemicalState('ATP')
ChemicalState.ADPPi = ChemicalState('ADP-Pi')
ChemicalState.ADP   = ChemicalState('ADP')

# Monomer mechanical state enumeration
class MechanicalState(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return "<MechanicalState: %s>" % self

MechanicalState.OPEN   = MechanicalState('Open')
MechanicalState.CLOSED = MechanicalState('Closed')
