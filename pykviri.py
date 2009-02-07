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
    """Kviri query constructor class"""

    def __init__(self, name=None):
        """
        >>> k = Kviri('x')
        >>> k._unused_name == 'x'
        True
        >>> k._bindings == [{}]
        True
        >>> k._results == None
        True

        >>> k = Kviri()
        >>> k._unused_name is None
        True
        >>> k._bindings == [{}]
        True
        >>> k._results == None
        True
        """

        self._unused_name = None
        self._unused_selectors = None
        self._bindings = [{}]
        self._results = None
        self.from_(name)

    def __iter__(self):
        if self._results is not None:
            return self._results.__iter__()
        else:
            return self._bindings.__iter__()

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

    def _get_selection(self, selectors, binding):
        """
        >>> k = Kviri()
        >>> k._get_selection(['x'], {'x': 1, 'y': 2})
        (1,)
        >>> k._get_selection(['x', 'y'], {'x': 1, 'y': 2})
        (1, 2)
        >>> k._get_selection(['y', 'x'], {'x': 1, 'y': 2})
        (2, 1)
        """

        result = []
        for selector in selectors:
            result.append(self._get_evaluation(selector, binding))
        return tuple(result)

    def _get_evaluation(self, code, binding=None):
        """
        >>> k = Kviri()
        >>> binding = {'x': 1}
        >>> k._get_evaluation('1 + 1')
        2
        >>> k._get_evaluation('1 + x', binding)
        2
        >>> binding
        {'x': 1}
        """

        if binding is None:
            binding = {}
        if callable(code):
            return code(**binding)
        else:
            return eval(code, binding.copy())


    def _filter(self, rule):
        """
        >>> Kviri('x').in_(range(10))._filter(lambda x, **rest: x % 2 == 0)
        [{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}]

        >>> Kviri('x').in_(range(10))._filter('x % 2 == 0')
        [{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}]
        """

        new_bindings = []
        for binding in self._bindings:
            if self._get_evaluation(rule, binding):
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

        orderings = reversed(orderings) # Sort by the last ordering first
        for ordering in orderings:
            if ordering.lower().endswith(' desc'):
                reverse = True
                ordering = ordering[:-len(' desc')]
            else:
                reverse = False
                if ordering.lower().endswith(' asc'):
                    ordering = ordering[:-len(' asc')]
            self._bindings.sort(key=lambda b: eval(ordering, b.copy()),
                reverse=reverse)
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
            self._results.append(self._get_selection(selectors, binding))
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

    def group(self, *selectors):
        """
        >>> k = Kviri().group('x', 'y')
        >>> k._unused_selectors
        ('x', 'y')
        """

        self._unused_selectors = selectors
        return self

    def by(self, criteria):
        """
        >>> k = Kviri('x').in_(range(10))
        >>> print k.group('x').by('x % 2')
        {0: [(0,), (2,), (4,), (6,), (8,)], 1: [(1,), (3,), (5,), (7,), (9,)]}

        >>> print k.from_('y').in_(('a', 'b')).group('x', 'y').by('x % 5')
        {0: [(0, 'a'), (5, 'a'), (0, 'b'), (5, 'b')],
         1: [(1, 'a'), (6, 'a'), (1, 'b'), (6, 'b')],
         2: [(2, 'a'), (7, 'a'), (2, 'b'), (7, 'b')],
         3: [(3, 'a'), (8, 'a'), (3, 'b'), (8, 'b')],
         4: [(4, 'a'), (9, 'a'), (4, 'b'), (9, 'b')]}
        """

        selectors = self._unused_selectors
        self._unused_selectors = None
        self._results = {}
        for binding in self._bindings:
            key = self._get_evaluation(criteria, binding)
            if key not in self._results:
                self._results[key] = []
            self._results[key].append(self._get_selection(selectors, binding))
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()
