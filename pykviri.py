#! /usr/bin/env python

import pprint

class Kviri(object):
    """
    Kviri -- LINQ for objects in Python

    >>> print Kviri('x').inSource(range(10)
    ...     ).where(lambda **n: n['x'] > 3 and n['x'] % 2 == 0
    ...     ).orderBy(('x', Kviri.DESC)
    ...     ).select('x')
    [{'x': 8}, {'x': 6}, {'x': 4}]
    """

    ASC=False
    DESC=True

    def __init__(self, name=None):
        """
        >>> k = Kviri('x')
        >>> k._unused_name == 'x'
        True
        >>> k.bindings == [{}]
        True
        >>> k.results == []
        True

        >>> k = Kviri()
        >>> k._unused_name is None
        True
        >>> k.bindings == [{}]
        True
        >>> k.results == []
        True
        """

        self._unused_name = None
        self.bindings = [{}]
        self.results = []
        self.fromName(name)

    def __repr__(self):
        return pprint.saferepr(self.results)

    def __str__(self):
        return pprint.pformat(self.results)

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
        >>> k.bindings
        [{'x': 0}, {'x': 1}, {'x': 2}]
        """

        name = self._get_name()
        new_bindings = []
        for value in source:
            for old_binding in self.bindings:
                new_binding = old_binding.copy()
                new_binding.update({name: value})
                new_bindings.append(new_binding)
        self.bindings = new_bindings
        return self

    let = _set_name

    def be(self, value):
        name = self._get_name()
        new_bindings = []
        for old_binding in self.bindings:
            new_binding = old_binding.copy()
            new_binding.update({name: value})
            new_bindings.append(new_binding)
        self.bindings = new_bindings
        return self

    def where(self, func):
        new_bindings = []
        for old_binding in self.bindings:
            if func(**old_binding):
                new_bindings.append(old_binding)
        self.bindings = new_bindings
        return self

    def orderBy(self, *orderings):
        for (order_key, reverse) in reversed(orderings):
            self.bindings.sort(key=lambda b: b[order_key], reverse=reverse)
        return self

    def select(self, *selectors):
        self.results = []
        for binding in self.bindings:
            result = []
            for i, selector in enumerate(selectors):
                if callable(selector):
                    result.append((i, selector(**binding)))
                else:
                    result.append((selector, binding[selector]))
            self.results.append(dict(result))
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()
