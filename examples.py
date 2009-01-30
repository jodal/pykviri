#! /usr/bin/env python

"""
Examples of Kviri usage
=======================

Before we begin
---------------

Import Kviri:

    >>> from pykviri import Kviri

Create some source collections:

    >>> L = [1, 2, 3]
    >>> M = [7, 8, 9]


Some simple queries
-------------------

FROM x IN L SELECT x:

    >>> Kviri('x').in_(L).select('x')
    [(1,), (2,), (3,)]

FROM x IN L WHERE x > 1 SELECT x:

    >>> Kviri('x').in_(L
    ...    ).where(lambda x, **rest: x > 1
    ...    ).select('x')
    [(2,), (3,)]

FROM x IN L FROM y IN M WHERE x > 1 SELECT x, y:

    >>> Kviri('x').in_(L
    ...    ).from_('y').in_(M
    ...    ).where(lambda x, **rest: x > 1
    ...    ).select('x', 'y')
    [(2, 7), (3, 7), (2, 8), (3, 8), (2, 9), (3, 9)]

A faster variant, as we filter as early as possible:

    >>> Kviri('x').in_(L
    ...    ).where(lambda x, **rest: x > 1
    ...    ).from_('y').in_(M
    ...    ).select('x', 'y')
    [(2, 7), (3, 7), (2, 8), (3, 8), (2, 9), (3, 9)]

And a bit simpler, using evaluated strings instead of lambdas:

    >>> Kviri('x').in_(L
    ...    ).where('x > 1'
    ...    ).from_('y').in_(M
    ...    ).select('x', 'y')
    [(2, 7), (3, 7), (2, 8), (3, 8), (2, 9), (3, 9)]

FROM x IN L FROM y in M WHERE x > 1 AND y in (8, 9) SELECT x, y:

    >>> Kviri('x').in_(L
    ...    ).from_('y').in_(M
    ...    ).where(lambda x, y, **rest: x > 1 and y in (8, 9)
    ...    ).select('x', 'y')
    [(2, 8), (3, 8), (2, 9), (3, 9)]


Adding constants
----------------

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z:

    >>> Kviri('x').in_(L
    ...    ).let('z').be(4
    ...    ).where(lambda x, **rest: x > 1
    ...    ).select('x', 'z')
    [(2, 4), (3, 4)]


Expressions in the result
-------------------------

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, x * z:

    >>> Kviri('x').in_(L
    ...    ).let('z').be(4
    ...    ).where(lambda x, **rest: x > 1
    ...    ).select('x', 'z', lambda x, z, **rest: x * z)
    [(2, 4, 8), (3, 4, 12)]

FROM x IN L LET z BE 4 WHERE x > 1 SELECT x, z, (x, z):

    >>> Kviri('x').in_(L
    ...    ).let('z').be(4
    ...    ).where(lambda x, **rest: x > 1
    ...    ).select('x', 'z', lambda x, z, **rest: (x, z))
    [(2, 4, (2, 4)), (3, 4, (3, 4))]

Or, simpler, as we use evaluated strings instead of lambdas.

    >>> Kviri('x').in_(L
    ...    ).let('z').be(4
    ...    ).where('x > 1'
    ...    ).select('x', 'z', '(x, z)')
    [(2, 4, (2, 4)), (3, 4, (3, 4))]


Ordering the results
--------------------

FROM x IN L ORDER BY x ASC SELECT x:

    >>> Kviri('x').in_(L
    ...    ).order_by('x'
    ...    ).select('x')
    [(1,), (2,), (3,)]

FROM x IN L ORDER BY x DESC SELECT x:

    >>> Kviri('x').in_(L
    ...    ).order_by('x desc'
    ...    ).select('x')
    [(3,), (2,), (1,)]

FROM x IN L FROM y IN M ORDER BY x DESC, y ASC SELECT x, y:

    >>> Kviri('x').in_(L
    ...    ).from_('y').in_(M
    ...    ).order_by('x desc', 'y asc'
    ...    ).select('x', 'y')
    [(3, 7), (3, 8), (3, 9), (2, 7), (2, 8), (2, 9), (1, 7), (1, 8), (1, 9)]


Only distinct results
---------------------

FROM x IN L FROM y IN M SELECT x:

    >>> Kviri('x').in_(L
    ...     ).from_('y').in_(M
    ...     ).select('x')
    [(1,), (2,), (3,), (1,), (2,), (3,), (1,), (2,), (3,)]

FROM x IN L FROM y IN M SELECT x DISTINCT:

    >>> Kviri('x').in_(L
    ...     ).from_('y').in_(M
    ...     ).select('x'
    ...     ).distinct()
    [(1,), (2,), (3,)]


Simple joins
------------

FROM x IN L JOIN y IN L ON (x == y) SELECT x, y:

    >>> Kviri('x').in_(L
    ...     ).join('y').in_(L).on(lambda x, y, **rest: x == y
    ...     ).select('x', 'y')
    [(1, 1), (2, 2), (3, 3)]

Or, using evaluated strings instead of lambdas.

    >>> Kviri('x').in_(L
    ...     ).join('y').in_(L).on('x == y'
    ...     ).select('x', 'y')
    [(1, 1), (2, 2), (3, 3)]


Working with objects
--------------------

Creating a class and some instances:

    >>> class Person(object):
    ...     def __init__(self, name, age):
    ...         self.name = name
    ...         self.age = age
    ...     def __repr__(self):
    ...         return 'Person(%s)' % self.name
    >>> persons = [
    ...     Person('Alice', 27),
    ...     Person('Bob', 28),
    ...     Person('Fred', 19),
    ...     Person('George', 19),
    ... ]

All persons of age 19:

    >>> Kviri('p').in_(persons).where('p.age == 19').select('p')
    [(Person(Fred),), (Person(George),)]

The names of everybody older than 21:

    >>> Kviri('p').in_(persons).where('p.age > 21').select('p.name')
    [('Alice',), ('Bob',)]

Everybody, ordered by age, then name:

    >>> Kviri('p').in_(persons).order_by('p.age', 'p.name').select('p')
    [(Person(Fred),), (Person(George),), (Person(Alice),), (Person(Bob),)]

Join people by age, but not with themselves:

    >>> Kviri('p').in_(persons
    ...     ).join('q').in_(persons).on('p.age == q.age and p is not q'
    ...     ).select('p', 'q')
    [(Person(George), Person(Fred)), (Person(Fred), Person(George))]


Building strings of the result
------------------------------

We can produce some more readable output directly:

    >>> Kviri('p').in_(persons
    ...     ).join('q').in_(persons).on('p.age == q.age and p is not q'
    ...     ).select('"%s is %d, and so is %s" % (p.name, p.age, q.name)')
    [('George is 19, and so is Fred',), ('Fred is 19, and so is George',)]

When we get to this complexity, lambdas may be preferable over evaluated
strings:

    >>> Kviri('p').in_(persons
    ...     ).join('q').in_(persons).on('p.age == q.age and p is not q'
    ...     ).select(lambda p, q: "%s is %d, and so is %s" % (
    ...              p.name, p.age, q.name))
    [('George is 19, and so is Fred',), ('Fred is 19, and so is George',)]


Iterating over the results
--------------------------

You can iterate over your Kviri query, just as if it was a list (though, this
example is rather stupid):

    >>> for i in Kviri('x').in_(L).select('x'):
    ...     print i
    (1,)
    (2,)
    (3,)

A query without a select() clause returns the bindings instead:

    >>> for i in Kviri('x').in_(L):
    ...     print i
    {'x': 1}
    {'x': 2}
    {'x': 3}


Grouping results
----------------

We can group results by some criteria:

    >>> Kviri('x').in_(L).group('x').by('x % 2')
    {0: [(2,)], 1: [(1,), (3,)]}

Or a bit more usefull:

    >>> print Kviri('p').in_(persons).group('p').by('p.age')
    {19: [(Person(Fred),), (Person(George),)],
     27: [(Person(Alice),)],
     28: [(Person(Bob),)]}

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
