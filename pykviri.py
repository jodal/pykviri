#! /usr/bin/env python

from pprint import pformat

class Kviri(object):
    ASC=False
    DESC=True

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
        for old_binding in self.bindings:
            for value in source:
                new_binding = old_binding.copy()
                new_binding.update({name: value})
                new_bindings.append(new_binding)
        self.bindings = new_bindings
        return self

    def let(self, name):
        self._set_name(name)
        return self

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

    def __repr__(self):
        return self.results

    def __str__(self):
        return pformat(self.results)

if __name__ == '__main__':
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
