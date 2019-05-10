from functools import wraps

def navbar(f):
    @wraps(f)
    def wrap_func(self):
        self.openNavBar()
        return f(self)
    return wrap_func