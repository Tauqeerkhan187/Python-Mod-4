# decorators.py
# decorator functions

import functools

def autosave(method):
    """
    Decorator for methods that modify the events list.
    After the wrapped method runs, the current calendar is saved
    via self.save().
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, *kwargs)
        # Only saves if the method didn't signal False
        if result is not False:
            self.save()
        return result
    return wrapper
