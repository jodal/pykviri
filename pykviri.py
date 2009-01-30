#! /usr/bin/env python

"""
Kviri -- LINQ for objects in Python

>>> print Kviri('x').in_(range(10)
...     ).where(lambda **n: n['x'] > 3 and n['x'] % 2 == 0
...     ).order_by(('x', Kviri.DESC)
...     ).select('x')
[(8,), (6,), (4,)]
"""

import pprint

class Kviri(object):
    ASC=False
    DESC=True

    def __init__(self, name=None):
        """
        >>> k = Kviri('x')
        >>> k._unused_name == 'x'
        True
        >>> k._bindings == [{}]
        True
        >>> k._results == []
        True

        >>> k = Kviri()
        >>> k._unused_name is None
        True
        >>> k._bindings == [{}]
        True
        >>> k._results == []
        True
        """

        self._unused_name = None
        self._bindings = [{}]
        self._results = []
        self.from_(name)

    def __repr__(self):
        return pprint.saferepr(self._results)

    def __str__(self):
        return pprint.pformat(self._results)

    def _get_name(self):
        """
        >>> k = Kviri('x')
        >>> k._unused_name == 'x'
        True
        >>> k._get_name()
        'x'
        >>> k._unused_name is None
        True
        """

        name = self._unused_name
        self._unused_name = None
        assert name is not None
        return name

    def _set_name(self, name):
        """
        >>> k = Kviri()
        >>> k._unused_name == None
        True
        >>> k._set_name('x')
        []
        >>> k._unused_name == 'x'
        True

        >>> k = Kviri('x')
        >>> k._unused_name == 'x'
        True
        >>> try:
        ...     k._set_name('x')
        ... except AssertionError:
        ...     print 'OK'
        OK
        >>> k._unused_name == 'x'
        True
        """

        assert self._unused_name is None
        self._unused_name = name
        return self

    from_ = _set_name

    def in_(self, source):
        """
        >>> k = Kviri('x').in_(range(3))
        >>> print k.select('x')
        [(0,), (1,), (2,)]
        """

        name = self._get_name()
        new_bindings = []
        for value in source:
            for old_binding in self._bindings:
                new_binding = old_binding.copy()
                new_binding.update({name: value})
                new_bindings.append(new_binding)
        self._bindings = new_bindings
        return self

    let = _set_name

    def be(self, value):
        """
        >>> k = Kviri('x').in_(range(2)).let('y').be(4)
        >>> print k.select('x', 'y')
        [(0, 4), (1, 4)]
        """

        name = self._get_name()
        new_bindings = []
        for old_binding in self._bindings:
            new_binding = old_binding.copy()
            new_binding.update({name: value})
            new_bindings.append(new_binding)
        self._bindings = new_bindings
        return self

    def where(self, func):
        """
        >>> k = Kviri('x').in_(range(10)).where(
        ...    lambda **n: n['x'] % 2 == 0)
        >>> print k.select('x')
        [(0,), (2,), (4,), (6,), (8,)]
        """

        new_bindings = []
        for old_binding in self._bindings:
            if func(**old_binding):
                new_bindings.append(old_binding)
        self._bindings = new_bindings
        return self

    def order_by(self, *orderings):
        """
        >>> k = Kviri('x').in_(range(3))
        >>> print k.order_by(('x', Kviri.DESC)).select('x')
        [(2,), (1,), (0,)]
        >>> print k.order_by(('x', Kviri.ASC)).select('x')
        [(0,), (1,), (2,)]
        >>> k2 = k.from_('y').in_(range(7, 9))
        >>> print k2.order_by(('y', Kviri.ASC), ('x', Kviri.ASC)
        ...     ).select('x', 'y')
        [(0, 7), (1, 7), (2, 7), (0, 8), (1, 8), (2, 8)]
        >>> k3 = Kviri('name').in_(('George', 'Fred', 'Mary', 'Bob'))
        >>> print k3.order_by(('name', Kviri.ASC)).select('name')
        [('Bob',), ('Fred',), ('George',), ('Mary',)]
        """

        orderings = reversed(orderings) # Sort by the last ordering first
        for (order_key, reverse) in orderings:
            self._bindings.sort(key=lambda b: b[order_key], reverse=reverse)
        return self

    def select(self, *selectors):
        """
        >>> k = Kviri('x').in_(range(3)
        ...     ).from_('y').in_(range(7, 9))
        >>> print k.select('x')
        [(0,), (1,), (2,), (0,), (1,), (2,)]
        >>> print k.select('y')
        [(7,), (7,), (7,), (8,), (8,), (8,)]
        >>> print k.select('x', 'y')
        [(0, 7), (1, 7), (2, 7), (0, 8), (1, 8), (2, 8)]
        >>> print k.select('x', 'y',
        ...     lambda **n: n['x'] + n['y'],
        ...     lambda **n: n['x'] * n['y'])
        [(0, 7, 7, 0),
         (1, 7, 8, 7),
         (2, 7, 9, 14),
         (0, 8, 8, 0),
         (1, 8, 9, 8),
         (2, 8, 10, 16)]
        """

        self._results = []
        for binding in self._bindings:
            result = []
            for i, selector in enumerate(selectors):
                if callable(selector):
                    result.append(selector(**binding))
                else:
                    result.append(binding[selector])
            self._results.append(tuple(result))
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()
