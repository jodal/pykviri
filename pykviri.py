#! /usr/bin/env python

"""
Kviri -- LINQ for objects in Python

>>> print Kviri('x').inSource(range(10)
...     ).where(lambda **n: n['x'] > 3 and n['x'] % 2 == 0
...     ).orderBy(('x', Kviri.DESC)
...     ).select('x')
[{'x': 8}, {'x': 6}, {'x': 4}]
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
        self.fromName(name)

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

    fromName = _set_name

    def inSource(self, source):
        """
        >>> k = Kviri('x').inSource(range(3))
        >>> print k.select('x')
        [{'x': 0}, {'x': 1}, {'x': 2}]
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
        >>> k = Kviri('x').inSource(range(2)).let('y').be(4)
        >>> print k.select('x', 'y')
        [{'x': 0, 'y': 4}, {'x': 1, 'y': 4}]
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
        >>> k = Kviri('x').inSource(range(10)).where(
        ...    lambda **n: n['x'] % 2 == 0)
        >>> print k.select('x')
        [{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}]
        """

        new_bindings = []
        for old_binding in self._bindings:
            if func(**old_binding):
                new_bindings.append(old_binding)
        self._bindings = new_bindings
        return self

    def orderBy(self, *orderings):
        """
        >>> k = Kviri('x').inSource(range(3))
        >>> print k.orderBy(('x', Kviri.DESC)).select('x')
        [{'x': 2}, {'x': 1}, {'x': 0}]
        >>> print k.orderBy(('x', Kviri.ASC)).select('x')
        [{'x': 0}, {'x': 1}, {'x': 2}]
        """

        for (order_key, reverse) in reversed(orderings):
            self._bindings.sort(key=lambda b: b[order_key], reverse=reverse)
        return self

    def select(self, *selectors):
        """
        >>> k = Kviri('x').inSource(range(3)
        ...     ).fromName('y').inSource(range(7, 9))
        >>> print k.select('x')
        [{'x': 0}, {'x': 1}, {'x': 2}, {'x': 0}, {'x': 1}, {'x': 2}]
        >>> print k.select('y')
        [{'y': 7}, {'y': 7}, {'y': 7}, {'y': 8}, {'y': 8}, {'y': 8}]
        >>> print k.select('x', 'y')
        [{'x': 0, 'y': 7},
         {'x': 1, 'y': 7},
         {'x': 2, 'y': 7},
         {'x': 0, 'y': 8},
         {'x': 1, 'y': 8},
         {'x': 2, 'y': 8}]
        >>> print k.select('x', 'y',
        ...     lambda **n: n['x'] + n['y'],
        ...     lambda **n: n['x'] * n['y'])
        [{2: 7, 3: 0, 'x': 0, 'y': 7},
         {2: 8, 3: 7, 'x': 1, 'y': 7},
         {2: 9, 3: 14, 'x': 2, 'y': 7},
         {2: 8, 3: 0, 'x': 0, 'y': 8},
         {2: 9, 3: 8, 'x': 1, 'y': 8},
         {2: 10, 3: 16, 'x': 2, 'y': 8}]
        """

        self._results = []
        for binding in self._bindings:
            result = []
            for i, selector in enumerate(selectors):
                if callable(selector):
                    result.append((i, selector(**binding)))
                else:
                    result.append((selector, binding[selector]))
            self._results.append(dict(result))
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()
