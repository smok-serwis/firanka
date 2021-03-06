from .base import Series


class FunctionSeries(Series):
    """
    Series with values defined by a function
    """

    def __init__(self, fun, domain, *args, **kwargs):
        super(FunctionSeries, self).__init__(domain, *args, **kwargs)
        self.fun = fun

    def _get_for(self, item):
        return self.fun(item)
