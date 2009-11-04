from states import ChemicalState

def strand_length( strand, added, removed, i ):
    return added - removed

def cap_length( strand, added, removed, i ):
    return strand.count_not(ChemicalState.ADP)

def ATP_cap( strand, added, removed, i ):
    return strand.count(ChemicalState.ATP)

def tip_state( strand, added, removed, i ):
    return strand.peek()
