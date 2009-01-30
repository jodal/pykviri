#! /usr/bin/env python

"""
Kviri -- LINQ for objects in Python

>>> Kviri('x').in_(range(10)
...     ).from_('y').in_(range(10)
...     ).where('x > 3 and (x + y) % 10 == 0'
...     ).order_by('x desc'
...     ).select('x', 'y')
[(9, 1), (8, 2), (7, 3), (6, 4), (5, 5), (4, 6)]
"""

import pprint

class Kviri(object):
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
        return pprint.saferepr(self._results or self._bindings)

    def __str__(self):
        return pprint.pformat(self._results or self._bindings)

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
        [{}]
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

    def _get_bindings_with_new(self, name, value):
        """
        >>> k = Kviri('x').in_(range(3))
        >>> k._bindings
        [{'x': 0}, {'x': 1}, {'x': 2}]
        >>> k._get_bindings_with_new('y', 3)
        [{'y': 3, 'x': 0}, {'y': 3, 'x': 1}, {'y': 3, 'x': 2}]
        """

        new_bindings = []
        for old_binding in self._bindings:
            new_binding = old_binding.copy()
            new_binding.update({name: value})
            new_bindings.append(new_binding)
        return new_bindings

    def _filter(self, filter):
        """
        >>> Kviri('x').in_(range(10))._filter(lambda x, **rest: x % 2 == 0)
        [{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}]

        >>> Kviri('x').in_(range(10))._filter('x % 2 == 0')
        [{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}]
        """

        new_bindings = []
        for binding in self._bindings:
            if callable(filter):
                if filter(**binding):
                    new_bindings.append(binding)
            elif eval(filter, binding.copy()):
                    new_bindings.append(binding)
        self._bindings = new_bindings
        return self

    from_ = _set_name

    def in_(self, source):
        """
        >>> Kviri('x').in_(range(3)).select('x')
        [(0,), (1,), (2,)]
        """

        name = self._get_name()
        new_bindings = []
        for value in source:
            new_bindings += self._get_bindings_with_new(name, value)
        self._bindings = new_bindings
        return self

    let = _set_name

    def be(self, value):
        """
        >>> Kviri('x').in_(range(2)).let('y').be(4).select('x', 'y')
        [(0, 4), (1, 4)]
        """

        name = self._get_name()
        self._bindings = self._get_bindings_with_new(name, value)
        return self

    join = _set_name
    on = _filter

    where = _filter

    def order_by(self, *orderings):
        """
        >>> k = Kviri('x').in_(range(3))
        >>> k.order_by('x').select('x')
        [(0,), (1,), (2,)]
        >>> k.order_by(('x DESC')).select('x')
        [(2,), (1,), (0,)]

        >>> k2 = k.from_('y').in_(range(7, 9))
        >>> k2.order_by('y AsC', 'x aSc').select('x', 'y')
        [(0, 7), (1, 7), (2, 7), (0, 8), (1, 8), (2, 8)]

        >>> Kviri('name').in_(('George', 'Fred', 'Mary', 'Bob')
        ...     ).order_by('name').select('name')
        [('Bob',), ('Fred',), ('George',), ('Mary',)]
        """

        def _get_key(binding):
            components = name.split('.', 1)
            key = components.pop(0)
            try:
                rest = components.pop(0)
                return eval('binding[key].%s' % rest)
            except IndexError:
                return binding[key]

        orderings = reversed(orderings) # Sort by the last ordering first
        for ordering in orderings:
            if ordering.lower().endswith(' desc'):
                reverse = True
                name = ordering[:-len(' desc')]
            else:
                reverse = False
                if ordering.lower().endswith(' asc'):
                    name = ordering[:-len(' asc')]
                else:
                    name = ordering
            self._bindings.sort(key=_get_key, reverse=reverse)
        return self

    def select(self, *selectors):
        """
        >>> k = Kviri('x').in_(range(3)
        ...     ).from_('y').in_(range(7, 9))
        >>> k.select('x')
        [(0,), (1,), (2,), (0,), (1,), (2,)]

        >>> k.select('y')
        [(7,), (7,), (7,), (8,), (8,), (8,)]

        >>> k.select('x', 'y')
        [(0, 7), (1, 7), (2, 7), (0, 8), (1, 8), (2, 8)]

        Using print makes the output more readable.

        >>> print k.select('x', 'y',
        ...     lambda x, y, **rest: x + y,
        ...     lambda **rest: rest['x'] * rest['y'])
        [(0, 7, 7, 0),
         (1, 7, 8, 7),
         (2, 7, 9, 14),
         (0, 8, 8, 0),
         (1, 8, 9, 8),
         (2, 8, 10, 16)]

        >>> print k.select('x', 'y', 'x + y', 'x * y')
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
                    result.append(eval(selector, binding.copy()))
            self._results.append(tuple(result))
        return self

    def distinct(self):
        """
        >>> k = Kviri('x').in_(range(3)
        ...     ).from_('y').in_(range(7, 9))
        >>> k.select('x')
        [(0,), (1,), (2,), (0,), (1,), (2,)]
        >>> k.select('x').distinct()
        [(0,), (1,), (2,)]
        """

        distinct_results = []
        for result in self._results:
            if result not in distinct_results:
                distinct_results.append(result)
        self._results = distinct_results
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()
