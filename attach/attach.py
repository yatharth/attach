import inspect
import textwrap
from typing import Dict


class DotDict(dict):
    """ Allow accessing/setting dictionary attributes with dot notation (e.g., `mydict.foo`) """

    def __getattr__(self, item):
        if item not in self.keys():
            raise KeyError(str(item))
        return dict.get(self, item)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getstate__(self):
        """ Enable pickling """
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self


class Namespace(DotDict):
    """ Serve as a namespace to store variables, suitable to use with `attach` below """

    def __repr__(self):
        MAX_WIDTH = 80
        PREFIX = " " * 4
        SUFFIX = ",\n"
        
        result = "Namespace({\n"
        for key, val in self.items():
            result += PREFIX + textwrap.shorten(
                "{}: {}".format(key, val),
                width = MAX_WIDTH - len(PREFIX) - len(SUFFIX),
                placeholder = "...") + SUFFIX 
            
        result += "})"
        return result


class attach():
    """ Context manager to attach and detach namespaces """

    def __init__(self, namespace, skip_underscored=True):
        assert isinstance(namespace, Dict)
        self.namespace = namespace
        self.skip_underscored = skip_underscored

    def __enter__(self):

        # Get the caller’s globals. The 0th frame is the current one.
        frames = inspect.stack()
        self.globals = frames[1].frame.f_globals

        # Backup globals and namespace.
        self.backup = self.globals.copy()

        for key, value in self.namespace.items():

            # Verify namespace does not collide with globals.
            if key in self.globals:
                raise RuntimeError("Namespace attribute '{}' collides with a global.".format(key))

            # Copy namespace to globals.
            self.globals[key] = value

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Delete namespace attributes that are no longer present.
        for key in set(self.namespace.keys()) - set(self.globals.keys()):
            del self.namespace[key]

        try:

            for key in self.globals.keys():

                # Copy globals back to namespace, skipping if underscored.
                if key not in self.backup:
                    if self.skip_underscored and key.startswith('_'):
                        continue
                    self.namespace[key] = self.globals[key]

                # Verify no pre-existing globals were modified.
                elif self.globals[key] is not self.backup[key]:
                    error_msg = "Modifying '{}' is prohibited because it was already a global.".format(key)
                    raise RuntimeError(error_msg) from exc_val

        # Restore globals.
        finally:
            self.globals.clear()
            self.globals.update(self.backup)

        # Indicate that this context manager does not handle exceptions,
        #  and they should not be suppressed.
        return False


""" Testing """

globals()['foo'] = 'global_foo'
globals().pop('bar', None)
globals().pop('baz', None)
globals().pop('biz', None)
globals().pop('_biz', None)

n = Namespace(foo='colliding_foo', bar='old_bar', baz='old_baz')

try:
    with attach(n):
        pass
except RuntimeError:
    pass
else:
    assert False, "Namespace shouldn't be able to collide with a global."

del n.foo

try:
    with attach(n):
        foo = 'new_foo'
except RuntimeError:
    pass
else:
    assert False, "Shouldn't be able to modify a pre-existing global."

with attach(n):
    assert bar == 'old_bar', "Accessing namespace"
    bar = 'new_bar'
    del baz
    biz = 'new_biz'
    _biz = 'new__biz'

assert n.get('bar') == 'new_bar', "Modifying pre-existing namespace attribute"
assert 'baz' not in n, "Deleting namespace attribute"
assert n.get('biz') == 'new_biz', "Adding a namespace attribute"
assert 'bar' not in globals() and 'baz' not in globals(), "Cleaning up globals"
assert '_biz' not in n, "Skipping over underscored variables"

m = Namespace()
with attach(m, skip_underscored=False):
    _biz = 'new__biz'
assert '_biz' in m, "Overriding skip_underscored default to False"
