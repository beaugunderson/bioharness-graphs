import matplotlib.pyplot as plt

from formatters import ShorterDateFormatter


def add_sleep_edges(ax, asleep, awake):
    """
    Add sleep and wake labels after the data has been plotted with the datetime
    index
    """
    # TODO: axvline
    ax.axvspan(asleep, asleep, edgecolor='purple')
    ax.axvspan(awake, awake, edgecolor='purple')


def add_sleep_labels(ax, asleep, awake):
    ax.annotate('Asleep',
                xy=(asleep, 100),
                xycoords='data',
                xytext=(15, 15),
                textcoords='offset points',
                arrowprops=dict(arrowstyle="-|>"))

    ax.annotate('Awake',
                xy=(awake, 100),
                xycoords='data',
                xytext=(-50, 15),
                textcoords='offset points',
                arrowprops=dict(arrowstyle="-|>"))


def make_labels_visible(ax):
    plt.setp(ax.get_xticklabels(), visible=True, rotation=0)


def center_tick_labels(ax):
    # Center the labels on their tick lines
    # TODO: Easier way to specify this?
    for label in ax.get_xticklabels():
        label.set_horizontalalignment('center')


def draw_bars(x, ax=None, **kwargs):
    ax = ax if ax is not None else plt.gca()
    ax.fill_between(x, 0, 1, antialiased=False, linewidth=1, **kwargs)

    if 'where' in kwargs:
        kwargs.pop('where')

    p = plt.Rectangle((0, 0), 0, 0, **kwargs)

    ax.add_patch(p)

    return p


def set_date_format(ax):
    ax.xaxis.set_major_formatter(ShorterDateFormatter)
