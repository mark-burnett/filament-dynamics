from numpy.random import mtrand
from strand import Strand, _join_strands, _evolve_substrand, _choose_state

# Basic tests of Strand object
# -------------------------------------------------------------------------
def test_empty():
    s = Strand( 0, None )
    assert( 0 == len(s) )
    assert( None == s.peek() )
    assert( 0 == s.count(None) )
    assert( 0 == s.count('a') )
    assert( 0 == s.count_not('a') )
    assert( 0 == s.count_not(None) )
    s.append('a')
    assert( 1 == len(s) )
    assert( 1 == s.count('a') )
    assert( 0 == s.count('b') )
    assert( 0 == s.count_not('a') )
    assert( 1 == s.count_not(None) )
    assert( 'a' == s.peek() )

def test_None():
    s = Strand( 1, None )
    assert( 1 == len(s) )
    assert( 1 == s.count(None) )
    assert( 0 == s.count_not(None) )
    assert( None == s.peek() )

def test_append():
    s = Strand( 10, 'tail' )
    assert( 10 == len(s) )
    s.append('append')
    assert( 11 == len(s) )
    s.append('append')
    s.append('append')
    s.append('append')
    s.append('append')
    assert( 15 == len(s) )
    assert( 5 == s.count('append') )
    assert( 10 == s.count_not('append') )

def test_pop():
    s = Strand( 10, 'tail' )
    assert( 10 == len(s) )
    p = s.pop()
    assert( 'tail' == p )
    assert(  9 == len(s) )
    s.append('pop')
    s.append('pop')
    assert( 11 == len(s) )
    assert( 'pop' == s.peek() )
    p2 = s.pop()
    assert( 'pop' == p2 )
    assert( 10 == len(s) )
    s.reverse()
    p3 = s.pop()
    assert( 'tail' == p3 )
    assert(  9 == len(s) )


def test_reverse():
    s = Strand( 3, 'tail' )
    s.append('append')
    assert( 'append' == s.peek() )
    s.reverse()
    assert( 'tail' == s.peek() )
    s.reverse()
    assert( 'append' == s.peek() )

# Test helper functions for hydrolysis
# -------------------------------------------------------------------------

# _join_strands tests
def test_join_strands_extend():
    L1 = [(3,'a'),(1,'b')]
    R1 = [(4,'c'),(5,'d')]
    T1 = _join_strands(L1, R1)
    assert( [(3,'a'), (1,'b'), (4,'c'), (5,'d')] == T1 )
    assert( [(3,'a'),(1,'b')] == L1 )
    assert( [(4,'c'),(5,'d')] == R1 )
    T2 = _join_strands(R1, L1)
    assert( [(4,'c'), (5,'d'), (3,'a'), (1,'b')] == T2 )
    assert( [(3,'a'),(1,'b')] == L1 )
    assert( [(4,'c'),(5,'d')] == R1 )

def test_join_strands_overlap():
    L1 = [(6,'a'),(3,'b')]
    R1 = [(1,'b'),(2,'a')]
    T1 = _join_strands(L1, R1)
    assert( [(6,'a'),(4,'b'),(2,'a')] == T1 )
    T2 = _join_strands(R1, L1)
    assert( [(1,'b'),(8,'a'),(3,'b')] == T2 )

def test_join_strands_empty():
    L1 = None
    R1 = [(6,'a'),(1,'b')]
    T1 = _join_strands(L1, R1)
    assert( T1 == R1 )
    L2 = [(3,'a'),(2,'b')]
    R2 = []
    T2 = _join_strands(L2, R2)
    assert( T2 == L2 )
    assert( [] == _join_strands( [], [] ) )

# _evolve_substrand tests
def test_evolve_substrand():
    from numpy.random import mtrand
    mtrand.seed(0)

    probs = [(0.1,'o1'),(0.2,'o2'),(0.3,'o3')]
    s1 = _evolve_substrand( (10, 'i'), probs)
    assert( [(10, 'i')] == s1 )
    s2 = _evolve_substrand( (10, 'i'), probs)
    assert( [(4, 'i'),(3,'o1'),(3,'i')] == s2 )
    s3 = _evolve_substrand( (10, 'i'), probs)
    assert( [(4, 'i'),(1,'o2'),(1,'i'),(1,'o2'),(3,'i')] == s3 )
    s4 = _evolve_substrand( (10, 'i'), probs)
    assert( [(1,'o3'),(3, 'i'),(1,'o1'),(5,'i')] == s4 )
    s5 = _evolve_substrand( (10, 'i'), probs)
    assert( [(3, 'i'),(1,'o1'),(2,'i'),(1,'o3'),(1,'o2'),(2,'i')] == s5 )

# _choose_state tests
def test_choose_state():
    probs = [(0.1,'o1'),(0.2,'o2'),(0.3,'o3')]
    assert( 'o1',      _choose_state(probs, 0.05, 'default') )
    assert( 'o1',      _choose_state(probs, 0.01, 'default') )
    assert( 'o2',      _choose_state(probs, 0.15, 'default') )
    assert( 'o3',      _choose_state(probs, 0.25, 'default') )
    assert( 'default', _choose_state(probs, 0.55, 'default') )

# Test overall Strand evolution
# -------------------------------------------------------------------------
def test_random_hydrolysis():
    mtrand.seed(0)

    probs = { ('s1', None): [(0.45,'s2')],
              ('s1', 's1'): [(0.45,'s2')],
              ('s1', 's2'): [(0.45,'s2')],
              ('s1', 's3'): [(0.45,'s2')],
              ('s2', None): [(0.1,'s3')],
              ('s2', 's1'): [(0.1,'s3')],
              ('s2', 's2'): [(0.1,'s3')],
              ('s2', 's3'): [(0.1,'s3')],
              ('s3', None): [],
              ('s3', 's1'): [],
              ('s3', 's2'): [],
              ('s3', 's3'): [] }

    s = Strand(10, 's1')
    # Reverse the substrands to be able to use the same test cases as before
    s.reverse()
    s.hydrolysis(probs)
    s.reverse()
    assert( [(4,'s1'),(1,'s2'),(1,'s1'),(1,'s2'),(2,'s1'),(1,'s2')]
            == s._substrands )
    s.reverse()
    s.hydrolysis(probs)
    s.reverse()
    assert( [(4,'s1'),(1,'s3'),(1,'s2'),(1,'s3'),(2,'s1'),(1,'s2')]
            == s._substrands )
    s.reverse()
    s.hydrolysis(probs)
    s.reverse()
    assert( [(4,'s1'),(1,'s3'),(1,'s2'),(1,'s3'),(1,'s1'),(2,'s2')]
            == s._substrands )
    s.reverse()
    s.hydrolysis(probs)
    s.reverse()
    assert( [(1,'s1'),(2,'s2'),(1,'s1'),(1,'s3'),(1,'s2'),(1,'s3'),(1,'s1'),
             (1,'s3'),(1,'s2')] == s._substrands )
    s.reverse()
    s.hydrolysis(probs)
    s.reverse()
    assert( [(1,'s1'),(2,'s2'),(1,'s1'),(1,'s3'),(1,'s2'),(1,'s3'),(1,'s2'),
             (1,'s3'),(1,'s2')] == s._substrands )
    s.reverse()
    s.hydrolysis(probs)
    s.reverse()
    assert( [(4,'s2'),(1,'s3'),(1,'s2'),(1,'s3'),(1,'s2'), (1,'s3'),(1,'s2')]
            == s._substrands )

def test_cooperative_hydrolysis():
    mtrand.seed(0)
    print mtrand.rand(2*8)
    mtrand.seed(0)
    probs = { ('s1', None): [(0.6,'s2')],
              ('s1', 's1'): [],
              ('s1', 's2'): [(0.6,'s2')],
              ('s1', 's3'): [(0.6,'s2')],
              ('s2', None): [(0.4,'s3')],
              ('s2', 's1'): [],
              ('s2', 's2'): [],
              ('s2', 's3'): [(0.4,'s3')],
              ('s3', None): [],
              ('s3', 's1'): [],
              ('s3', 's2'): [],
              ('s3', 's3'): [] }

    s = Strand(10, 's1')
    s._substrands = [(10, 's3'), (10, 's2'), (10,'s1')]

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(10, 's3'),(11, 's2'),( 9, 's1')] == s._substrands )

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(10, 's3'),(11, 's2'),( 9, 's1')] == s._substrands )

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(10, 's3'),(12, 's2'),( 8, 's1')] == s._substrands )

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(10, 's3'),(13, 's2'),( 7, 's1')] == s._substrands )

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(11, 's3'),(12, 's2'),( 7, 's1')] == s._substrands )

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(11, 's3'),(12, 's2'),( 7, 's1')] == s._substrands )

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(11, 's3'),(13, 's2'),( 6, 's1')] == s._substrands )

    s.hydrolysis(probs)
    print s._substrands
    assert( 30 == len(s) )
    assert(  3 == len(s._substrands) )
    assert( [(12, 's3'),(13, 's2'),( 5, 's1')] == s._substrands )
