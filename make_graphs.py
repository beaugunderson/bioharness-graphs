#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas

import graphs

from utilities import (make_labels_visible, center_tick_labels,
                       set_date_format, add_sleep_edges, add_sleep_labels)

# get_ipython().magic(u'matplotlib inline')
# get_ipython().magic(u"config InlineBackend.figure_format = 'retina'")

# matplotlib.rcParams['figure.facecolor'] = 'white'


def graph_bioharness_data(data, asleep, awake, filename='output.png'):
    fig = plt.figure(figsize=(14, 16))

    fig.set_dpi(220)
    # fig.set_tight_layout(True)

    SIZE = (7, 2)

    heart_rate_ax = plt.subplot2grid(SIZE, (0, 0), colspan=2)
    hrv_ax = plt.subplot2grid(SIZE, (1, 0), colspan=2)
    breath_rate_ax = plt.subplot2grid(SIZE, (2, 0), colspan=2)
    temperature_ax = plt.subplot2grid(SIZE, (3, 0), colspan=2)
    activity_ax = plt.subplot2grid(SIZE, (4, 0), colspan=2)
    position_ax = plt.subplot2grid(SIZE, (5, 0), colspan=2)

    hr_probability_ax = plt.subplot2grid(SIZE, (6, 0))
    hr_histogram_ax = plt.subplot2grid(SIZE, (6, 1))

    ALL_AXES = [heart_rate_ax, hrv_ax, breath_rate_ax, temperature_ax,
                activity_ax, position_ax, hr_probability_ax, hr_histogram_ax]

    DATE_AXES = [heart_rate_ax, hrv_ax, breath_rate_ax, temperature_ax,
                 activity_ax, position_ax]

    graphs.heart_rate(heart_rate_ax, data)
    graphs.hrv(hrv_ax, data.HRV)
    graphs.breath_rate(breath_rate_ax, data)
    graphs.temperature(temperature_ax, data)
    graphs.activity(activity_ax, data)
    graphs.position(position_ax, data)

    graphs.hr_stats(hr_probability_ax, hr_histogram_ax, data)

    for ax in DATE_AXES:
        center_tick_labels(ax)
        set_date_format(ax)

        add_sleep_edges(ax, asleep, awake)

    add_sleep_labels(heart_rate_ax, asleep, awake)

    for ax in ALL_AXES:
        make_labels_visible(ax)

    # Add some extra space for labels
    fig.subplots_adjust(hspace=0.35)

    fig.tight_layout()

    plt.savefig(filename, bbox_inches='tight')


def render_file(filename):
    asleep = '3/13/2015 11:56pm'
    awake = '3/14/2015 8:23am'

    data = pandas.DataFrame.from_csv(filename, parse_dates=True)

    graph_bioharness_data(data, asleep, awake)

    #filtered_data = filtered_data[
    #    (data.HR < 150) & (data.HR > 0) &
    #    (data.HRConfidence > 50) &
    #    (data.BR < 500) & (data.BR > 0)
    #]

    #filtered_data[
    #    ((data.HR > 150) | (data.HR < 50)) |
    #    (data.HRConfidence < 75) |
    #    ((data.BR > 500) | (data.BR < 3))
    #] = NaN

    #filtered_data = filtered_data.where(data['HR'] < 150)
    #filtered_data.loc(filtered_data.HR < 80)['HR'] = 0
    #filtered_data.fillna(0)


if __name__ == '__main__':
    # summary = './2015.03.12/Record 4_2015_03_12-01_55_25_Summary.csv'
    # summary = './2015.03.13/2015_03_13-23_41_16_Summary.csv'
    summary = './2015.03.14/2015_03_14-22_15_55_Summary.csv'

    render_file(summary)
