#!/usr/bin/env python

from __future__ import division

import itertools
import matplotlib.pyplot as plt
import numpy
import pandas
import seaborn

from itertools import izip_longest

from scipy.signal import butter, lfilter

ratio = 0.078125
width = 24
height = width * ratio


def filter_butter(series):
    order = 4 # filter order
    f = 35.0000 # cutoff frequency
    fs = 250 # sampling frequency # was 500

    # Apply Butterworth filter to raw signal
    [b, a] = butter(order, f / fs, 'low') # Get Butterworth Filter Coefficients

    # Filter the signal using extracted coefficients
    return lfilter(b, a, series)


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n

    return izip_longest(fillvalue=fillvalue, *args)


def graph_ecg(filename):
    print 'Reading file...'
    data = pandas.io.parsers.read_csv(filename,
                                      parse_dates=[0],
                                      index_col='Time',
                                      infer_datetime_format=True)
                                      # nrows=250000)

    print 'Filtering...'
    data.EcgWaveform = filter_butter(data.EcgWaveform)

    print 'Grouping...'
    unfiltered_groups = data.groupby(pandas.Grouper(freq='20s'))

    def point_ratio(points):
        good_points = numpy.sum((points > 1900) & (points < 2400))

        return good_points / len(points)

    all_groups = [g for _, g in unfiltered_groups
                  if point_ratio(g.EcgWaveform) > 0.8]

    sub_groups = grouper(all_groups, 24)

    for i, groups in enumerate(sub_groups, start=1):
        num_groups = len(groups)

        fig, axes = plt.subplots(num_groups,
                                 figsize=(width, num_groups * height))

        fig.set_dpi(300)

        print '{}: Iterating {} groups...'.format(i, num_groups)

        for ax, group in itertools.izip(axes, groups):
            ax.plot(group.index.to_pydatetime(), group.EcgWaveform, lw=0.8)

            ax.set_ylim(1900, 2400)

        fig.tight_layout()

        print 'Saving epochs_{}.png...'
        plt.savefig('epochs_{}.png'.format(i), bbox_inches='tight')


if __name__ == '__main__':
    ecg_file = './2015.03.13/2015_03_13-23_41_16_ECG.csv'

    graph_ecg(ecg_file)
