from firanka.series import FunctionSeries

NOOP = lambda x: x
HUGE_IDENTITY = FunctionSeries(NOOP, '(-inf;inf)')
