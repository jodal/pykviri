#! /usr/bin/env python

"""
Examples on Kviri usage
=======================

>>> from pykviri import Kviri
>>> L = [1, 2, 3]
>>> M = [7, 8, 9]

FROM x IN L WHERE x > 1 SELECT x:

>>> print Kviri('x').inSource(L
...    ).where(lambda **names: names['x'] > 1
...    ).select('x')
[{'x': 2}, {'x': 3}]

FROM x IN L WHERE x > 1 FROM y in M SELECT x, y:

>>> print Kviri('x').inSource(L
...    ).where(lambda **names: names['x'] > 1
...    ).fromName('y').inSource(M
...    ).select('x', 'y')
[{'x': 2, 'y': 7},
 {'x': 2, 'y': 8},
 {'x': 2, 'y': 9},
 {'x': 3, 'y': 7},
 {'x': 3, 'y': 8},
 {'x': 3, 'y': 9}]

FROM x IN L FROM y IN M WHERE x > 1 SELECT x, y:

>>> print Kviri('x').inSource(L
...    ).fromName('y').inSource(M
...    ).where(lambda **names: names['x'] > 1
...    ).select('x', 'y')
[{'x': 2, 'y': 7},
 {'x': 2, 'y': 8},
 {'x': 2, 'y': 9},
 {'x': 3, 'y': 7},
 {'x': 3, 'y': 8},
 {'x': 3, 'y': 9}]

FROM x IN L FROM y in M WHERE x > 1 AND y in (8, 9) SELECT x, y:

>>> print Kviri('x').inSource(L
...    ).fromName('y').inSource(M
...    ).where(lambda **names: names['x'] > 1 and names['y'] in (8, 9)
...    ).select('x', 'y')
[{'x': 2, 'y': 8}, {'x': 2, 'y': 9}, {'x': 3, 'y': 8}, {'x': 3, 'y': 9}]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z:

>>> print Kviri('x').inSource(L
...    ).let('z').be(4
...    ).where(lambda **names: names['x'] > 1
...    ).select('x', 'z')
[{'x': 2, 'z': 4}, {'x': 3, 'z': 4}]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, x * z:

>>> print Kviri('x').inSource(L
...    ).let('z').be(4
...    ).where(lambda **names: names['x'] > 1
...    ).select('x', 'z',
...        lambda **names: names['x'] * names['z'])
[{2: 8, 'x': 2, 'z': 4}, {2: 12, 'x': 3, 'z': 4}]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, (x, z):

>>> print Kviri('x').inSource(L
...    ).let('z').be(4
...    ).where(lambda **names: names['x'] > 1
...    ).select('x', 'z',
...        lambda **names: (names['x'], names['z']))
[{2: (2, 4), 'x': 2, 'z': 4}, {2: (3, 4), 'x': 3, 'z': 4}]

FROM x IN L ORDER BY x ASC SELECT x:

>>> print Kviri('x').inSource(L
...    ).orderBy(('x', Kviri.ASC)
...    ).select('x')
[{'x': 1}, {'x': 2}, {'x': 3}]

FROM x IN L ORDER BY x DESC SELECT x:

>>> print Kviri('x').inSource(L
...    ).orderBy(('x', Kviri.DESC)
...    ).select('x')
[{'x': 3}, {'x': 2}, {'x': 1}]

FROM x IN L FROM y in M ORDER BY x DESC, y DESC SELECT x, y:

>>> print Kviri('x').inSource(L
...    ).fromName('y').inSource(M
...    ).orderBy(('x', Kviri.DESC), ('y', Kviri.DESC)
...    ).select('x', 'y')
[{'x': 3, 'y': 9},
 {'x': 3, 'y': 8},
 {'x': 3, 'y': 7},
 {'x': 2, 'y': 9},
 {'x': 2, 'y': 8},
 {'x': 2, 'y': 7},
 {'x': 1, 'y': 9},
 {'x': 1, 'y': 8},
 {'x': 1, 'y': 7}]

FROM x IN L FROM y in M ORDER BY x DESC, y ASC SELECT x, y:

>>> print Kviri('x').inSource(L
...    ).fromName('y').inSource(M
...    ).orderBy(('x', Kviri.DESC), ('y', Kviri.ASC)
...    ).select('x', 'y')
[{'x': 3, 'y': 7},
 {'x': 3, 'y': 8},
 {'x': 3, 'y': 9},
 {'x': 2, 'y': 7},
 {'x': 2, 'y': 8},
 {'x': 2, 'y': 9},
 {'x': 1, 'y': 7},
 {'x': 1, 'y': 8},
 {'x': 1, 'y': 9}]

FROM x IN L FROM y in M ORDER BY x ASC, y DESC SELECT x, y

>>> print Kviri('x').inSource(L
...    ).fromName('y').inSource(M
...    ).orderBy(('x', Kviri.ASC), ('y', Kviri.DESC)
...    ).select('x', 'y')
[{'x': 1, 'y': 9},
 {'x': 1, 'y': 8},
 {'x': 1, 'y': 7},
 {'x': 2, 'y': 9},
 {'x': 2, 'y': 8},
 {'x': 2, 'y': 7},
 {'x': 3, 'y': 9},
 {'x': 3, 'y': 8},
 {'x': 3, 'y': 7}]

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
