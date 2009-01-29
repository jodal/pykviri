#! /usr/bin/env python

from pykviri import Kviri

L = [1, 2, 3]
M = [7, 8, 9]
print 'L=%s, M=%s' % (L, M)

print 'FROM x IN L WHERE x > 1 SELECT x:'
print Kviri('x').inSource(L
    ).where(lambda **names: names['x'] > 1
    ).select('x')

print 'FROM x IN L WHERE x > 1 FROM y in M SELECT x, y:'
print Kviri('x').inSource(L
    ).where(lambda **names: names['x'] > 1
    ).andFrom('y').inSource(M
    ).select('x', 'y')

print 'FROM x IN L FROM y IN M WHERE x > 1 SELECT x, y:'
print Kviri('x').inSource(L
    ).andFrom('y').inSource(M
    ).where(lambda **names: names['x'] > 1
    ).select('x', 'y')

print 'FROM x IN L FROM y in M WHERE x > 1 AND y in (8, 9) SELECT x, y:'
print Kviri('x').inSource(L
    ).andFrom('y').inSource(M
    ).where(lambda **names: names['x'] > 1 and names['y'] in (8, 9)
    ).select('x', 'y')

print 'FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z:'
print Kviri('x').inSource(L
    ).let('z').be(4
    ).where(lambda **names: names['x'] > 1
    ).select('x', 'z')

print 'FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, x * z:'
print Kviri('x').inSource(L
    ).let('z').be(4
    ).where(lambda **names: names['x'] > 1
    ).select('x', 'z',
        lambda **names: names['x'] * names['z'])

print 'FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, (x, z):'
print Kviri('x').inSource(L
    ).let('z').be(4
    ).where(lambda **names: names['x'] > 1
    ).select('x', 'z',
        lambda **names: (names['x'], names['z']))

print 'FROM x IN L ORDER BY x ASC SELECT x'
print Kviri('x').inSource(L
    ).orderBy(('x', Kviri.ASC)
    ).select('x')

print 'FROM x IN L ORDER BY x DESC SELECT x'
print Kviri('x').inSource(L
    ).orderBy(('x', Kviri.DESC)
    ).select('x')

print 'FROM x IN L FROM y in M ORDER BY x DESC, y DESC SELECT x, y'
print Kviri('x').inSource(L
    ).andFrom('y').inSource(M
    ).orderBy(('x', Kviri.DESC), ('y', Kviri.DESC)
    ).select('x', 'y')

print 'FROM x IN L FROM y in M ORDER BY x DESC, y ASC SELECT x, y'
print Kviri('x').inSource(L
    ).andFrom('y').inSource(M
    ).orderBy(('x', Kviri.DESC), ('y', Kviri.ASC)
    ).select('x', 'y')

print 'FROM x IN L FROM y in M ORDER BY x ASC, y DESC SELECT x, y'
print Kviri('x').inSource(L
    ).andFrom('y').inSource(M
    ).orderBy(('x', Kviri.ASC), ('y', Kviri.DESC)
    ).select('x', 'y')
