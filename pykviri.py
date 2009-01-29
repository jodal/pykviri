#! /usr/bin/env python

from pprint import pformat

class Kviri(object):
    def __init__(self, name):
        self._unused_name = None
        self.bindings = [{}]
        self.results = None
        self.andFrom(name)

    def _set_name(self, name):
        assert self._unused_name is None
        self._unused_name = name

    def _get_name(self):
        name = self._unused_name
        self._unused_name = None
        assert name is not None
        return name

    def andFrom(self, name):
        self._set_name(name)
        return self

    def inSource(self, source):
        name = self._get_name()
        new_bindings = []
        for b in self.bindings:
            for s in source:
                new_binding = b.copy()
                new_binding.update({name: s})
                new_bindings.append(new_binding)
        self.bindings = new_bindings
        return self

    def let(self, name):
        self._set_name(name)
        return self

    def be(self, value):
        name = self._get_name()
        new_bindings = []
        for b in self.bindings:
            new_binding = b.copy()
            new_binding.update({name: value})
            new_bindings.append(new_binding)
        self.bindings = new_bindings
        return self

    def where(self, func):
        new_bindings = []
        for b in self.bindings:
            if func(**b):
                new_bindings.append(b)
        self.bindings = new_bindings
        return self

    def orderBy(self, *orderings):
        # FIXME Support ordering by multiple columns
        for (o, reverse) in orderings:
            self.bindings.sort(key=lambda b: b[o], reverse=reverse)
        return self

    def select(self, *selectors):
        self.results = []
        for b in self.bindings:
            result = []
            for i, s in enumerate(selectors):
                if callable(s):
                    result.append((i, s(**b)))
                else:
                    result.append((s, b[s]))
            self.results.append(dict(result))
        return self

    def __repr__(self):
        return self.results

    def __str__(self):
        return pformat(self.results)

if __name__ == '__main__':
    L = [1, 2, 3]
    M = [7, 8, 9]
    print Kviri('x').inSource(L
        ).where(lambda **names: names['x'] > 1
        ).select('x')
    print Kviri('x').inSource(L
        ).where(lambda **names: names['x'] > 1
        ).andFrom('y').inSource(M
        ).select('x', 'y')
    print Kviri('x').inSource(L
        ).andFrom('y').inSource(M
        ).where(lambda **names: names['x'] > 1
        ).select('x', 'y')
    print Kviri('x').inSource(L
        ).andFrom('y').inSource(M
        ).where(lambda **names: names['x'] > 1 and names['y'] in (8, 9)
        ).select('x', 'y')
    print Kviri('x').inSource(L
        ).andFrom('y').inSource(M
        ).let('z').be(4
        ).where(lambda **names: names['x'] > 1
        ).select('x', 'y', 'z')
    print Kviri('x').inSource(L
        ).andFrom('y').inSource(M
        ).let('z').be(4
        ).where(lambda **names: names['x'] > 1
        ).select('x', 'y', 'z',
            lambda **names: names['x'] * names['y'] * names['z'])
    print Kviri('x').inSource(L + M
        ).orderBy(('x', False)
        ).select('x')
    print Kviri('x').inSource(L + M
        ).orderBy(('x', True)
        ).select('x')
