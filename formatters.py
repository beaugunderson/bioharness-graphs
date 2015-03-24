import matplotlib.dates as dates

from matplotlib.ticker import FuncFormatter

def to_percent(y, position):
    return str(100 * y) + '%'

PercentFormatter = FuncFormatter(to_percent)

ShortDateFormatter = dates.DateFormatter('%I:%M%p')

def shorten_date(x, position):
    return ShortDateFormatter(x, position).lower().lstrip('0')

ShorterDateFormatter = FuncFormatter(shorten_date)
