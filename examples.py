#! /usr/bin/env python

"""
Examples on Kviri usage
=======================

>>> from pykviri import Kviri
>>> L = [1, 2, 3]
>>> M = [7, 8, 9]

FROM x IN L WHERE x > 1 SELECT x:

>>> print Kviri('x').in_(L
...    ).where(lambda x, **rest: x > 1
...    ).select('x')
[(2,), (3,)]

FROM x IN L FROM y IN M WHERE x > 1 SELECT x, y:

>>> print Kviri('x').in_(L
...    ).from_('y').in_(M
...    ).where(lambda x, **rest: x > 1
...    ).select('x', 'y')
[(2, 7), (3, 7), (2, 8), (3, 8), (2, 9), (3, 9)]

FROM x IN L WHERE x > 1 FROM y in M SELECT x, y:
Faster, as we filter as early as possible.

>>> print Kviri('x').in_(L
...    ).where(lambda x, **rest: x > 1
...    ).from_('y').in_(M
...    ).select('x', 'y')
[(2, 7), (3, 7), (2, 8), (3, 8), (2, 9), (3, 9)]

FROM x IN L WHERE x > 1 FROM y in M SELECT x, y:
Simpler where(), as string is evaluated in context of the bindings.

>>> print Kviri('x').in_(L
...    ).where('x > 1'
...    ).from_('y').in_(M
...    ).select('x', 'y')
[(2, 7), (3, 7), (2, 8), (3, 8), (2, 9), (3, 9)]

FROM x IN L FROM y in M WHERE x > 1 AND y in (8, 9) SELECT x, y:

>>> print Kviri('x').in_(L
...    ).from_('y').in_(M
...    ).where(lambda x, y, **rest: x > 1 and y in (8, 9)
...    ).select('x', 'y')
[(2, 8), (3, 8), (2, 9), (3, 9)]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z:

>>> print Kviri('x').in_(L
...    ).let('z').be(4
...    ).where(lambda x, **rest: x > 1
...    ).select('x', 'z')
[(2, 4), (3, 4)]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, x * z:

>>> print Kviri('x').in_(L
...    ).let('z').be(4
...    ).where(lambda x, **rest: x > 1
...    ).select('x', 'z', lambda x, z, **rest: x * z)
[(2, 4, 8), (3, 4, 12)]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, (x, z):

>>> print Kviri('x').in_(L
...    ).let('z').be(4
...    ).where(lambda **names: names['x'] > 1
...    ).select('x', 'z', lambda x, z, **rest: (x, z))
[(2, 4, (2, 4)), (3, 4, (3, 4))]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, (x, z):
Simpler, as we use evaluated strings instead of lambdas.

>>> print Kviri('x').in_(L
...    ).let('z').be(4
...    ).where('x > 1'
...    ).select('x', 'z', '(x, z)')
[(2, 4, (2, 4)), (3, 4, (3, 4))]

FROM x IN L ORDER BY x ASC SELECT x:

>>> print Kviri('x').in_(L
...    ).order_by('x'
...    ).select('x')
[(1,), (2,), (3,)]

FROM x IN L ORDER BY x DESC SELECT x:

>>> print Kviri('x').in_(L
...    ).order_by('x desc'
...    ).select('x')
[(3,), (2,), (1,)]

FROM x IN L FROM y IN M ORDER BY x DESC, y DESC SELECT x, y:

>>> print Kviri('x').in_(L
...    ).from_('y').in_(M
...    ).order_by('x desc', 'y desc'
...    ).select('x', 'y')
[(3, 9), (3, 8), (3, 7), (2, 9), (2, 8), (2, 7), (1, 9), (1, 8), (1, 7)]

FROM x IN L FROM y IN M ORDER BY x DESC, y ASC SELECT x, y:

>>> print Kviri('x').in_(L
...    ).from_('y').in_(M
...    ).order_by('x desc', 'y asc'
...    ).select('x', 'y')
[(3, 7), (3, 8), (3, 9), (2, 7), (2, 8), (2, 9), (1, 7), (1, 8), (1, 9)]

FROM x IN L FROM y IN M ORDER BY x ASC, y DESC SELECT x, y:

>>> print Kviri('x').in_(L
...    ).from_('y').in_(M
...    ).order_by('x asc', 'y desc'
...    ).select('x', 'y')
[(1, 9), (1, 8), (1, 7), (2, 9), (2, 8), (2, 7), (3, 9), (3, 8), (3, 7)]

FROM x IN L FROM y IN M SELECT x DISTINCT:

>>> print Kviri('x').in_(L
...     ).from_('y').in_(M
...     ).select('x'
...     ).distinct()
[(1,), (2,), (3,)]

FROM x IN L JOIN y IN L ON (x == y) SELECT x, y:

>>> print Kviri('x').in_(L
...     ).join('y').in_(L).on(lambda x, y, **rest: x == y
...     ).select('x', 'y')
[(1, 1), (2, 2), (3, 3)]

FROM x IN L JOIN y IN L ON (x == y) SELECT x, y:
Using strings instead of lambdas.

>>> print Kviri('x').in_(L
...     ).join('y').in_(L).on('x == y'
...     ).select('x', 'y')
[(1, 1), (2, 2), (3, 3)]

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
