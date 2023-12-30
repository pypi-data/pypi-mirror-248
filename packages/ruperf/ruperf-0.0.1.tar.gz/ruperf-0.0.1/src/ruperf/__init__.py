__version__ = "0.0.1"

import time
import contextlib


class Profiler(contextlib.ContextDecorator):
    """This for a simple Profiler from python"""

    def __init__(self, desc=None, verbose=True, logger=None, precision=None):
        self.verbose = verbose
        self.prefix = f"🥝 :: {desc or 'Profiler'} => "
        self.logger = logger or print
        self.precision = precision
        # self._elapsed = None

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, type, value, traceback):
        if self.verbose:
            self.log(time.time() - self.t0)

    def __call__(self, obj):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            ret = obj(*args, **kwargs)
            if self.verbose:
                self.log(time.time() - t0)
            return ret
        return wrapper


    def log(self, _t):
        unit = 's'
        if _t < 1:
            _t *= 1e3
            unit = 'ms'
        _s = f"{self.prefix}{_t:.{self.precision or 10}f}" + unit
        self.logger(_s)


    # def elapsed(self):
    #     self._elapsed



__all__ = [
    "__version__",
    "Profiler"
]
