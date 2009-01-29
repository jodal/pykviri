from pprint import pformat

class Kviri(object):
    ASC=False
    DESC=True

    def __init__(self, name):
        self._unused_name = None
        self.bindings = [{}]
        self.results = None
        self.fromName(name)

    def __repr__(self):
        return self.results

    def __str__(self):
        return pformat(self.results)

    def _set_name(self, name):
        assert self._unused_name is None
        self._unused_name = name

    def _get_name(self):
        name = self._unused_name
        self._unused_name = None
        assert name is not None
        return name

    def fromName(self, name):
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
