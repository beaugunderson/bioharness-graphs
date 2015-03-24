import matplotlib.transforms as mtransforms
import numpy
import pandas
import seaborn

from formatters import PercentFormatter
from utilities import draw_bars

ewma = pandas.stats.moments.ewma


SPAN = 5 * 60


def hrv(ax, data):
    hrv_mask = data < 1000
    hrv_no_nan = data.where(hrv_mask)

    ewma(hrv_no_nan, span=SPAN, ignore_na=True).where(hrv_mask).plot(
        ax=ax, lw=0.5, title='Heart Rate Variability')


def heart_rate(ax, data):
    # use the data coordinates for the x-axis and the axes coordinates for the
    # y-axis
    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)

    MINIMUM_CONFIDENCE = 75.0

    ax.set_ylim(bottom=50, top=140)

    ax.fill_between(data.index, 0, 1,
                    where=data.HRConfidence >= MINIMUM_CONFIDENCE,
                    facecolor='#BDFCC7', transform=trans, linewidth=1,
                    edgecolor='#BDFCC7', antialiased=False)

    ax.fill_between(data.index, 0, 1,
                    where=data.HRConfidence < MINIMUM_CONFIDENCE,
                    facecolor='#FCBDBD', transform=trans, linewidth=1,
                    edgecolor='#FCBDBD', antialiased=False)

    #data.HR.plot(ax=axes[0], color='b', lw=0.5)
    ewma(data.HR, span=SPAN, ignore_na=True).plot(ax=ax, color='black',
                                                lw=0.5,
                                                title='Beats per Minute')

    ax.axhline(y=100, lw=0.5)


def temperature(ax, data):
    def to_fahrenheit(celsius):
        return 1.8 * celsius + 32

    data.CoreTemp = data.CoreTemp.map(to_fahrenheit)
    data.DeviceTemp = data.DeviceTemp.map(to_fahrenheit)

    high_confidence = data.query('HRConfidence >= 95')

    ewma(data.CoreTemp,
         span=SPAN).plot(ax=ax, lw=0.5, title='Temperature', label='Core')
    ewma(data.DeviceTemp,
         span=SPAN).plot(ax=ax, lw=0.5, label='Device')

    temp_min = min((high_confidence.CoreTemp.min(),
                    high_confidence.DeviceTemp.min())) - 3

    temp_max = max((high_confidence.CoreTemp.max(),
                    high_confidence.DeviceTemp.max())) + 3

    temp_min = max(temp_min, 50)
    temp_max = min(temp_max, 105)

    ax.set_ylim(bottom=temp_min, top=temp_max)
    ax.legend()


def breath_rate(ax, data):
    ax.set_ylim(bottom=0, top=40)

    ewma(data.BR, span=SPAN).plot(ax=ax, lw=0.5, title='Breaths per Minute')


def activity(ax, data):
    activity_percentage = data.Activity * 100

    ewma(activity_percentage, span=SPAN).plot(ax=ax, lw=0.5,
                                            title='Activity Level / Posture')

    # axes[3].set_yscale('log', basey=10)
    ax.set_ylim(activity_percentage.min(), activity_percentage.max())

    ewma(data.Posture, span=SPAN).plot(secondary_y=True, ax=ax, lw=0.5)


def position(ax, data):
    # Sagittal (Lateral) = SagittalPeak
    # Transverse (Axial, Horizontal) = VerticalPeak
    # Frontal (Coronal) = LateralPeak

    Sagittal = data.SagittalPeak
    Transverse = data.VerticalPeak
    Frontal = data.LateralPeak

    ewma(Sagittal, span=SPAN).plot(ax=ax,
                                 lw=0.5,
                                 label='Sagittal',
                                 alpha=0.25,
                                 color='black')

    ewma(Transverse, span=SPAN).plot(ax=ax,
                                   lw=0.5,
                                   label='Transverse',
                                   alpha=0.25,
                                   color='black')

    ewma(Frontal, span=SPAN).plot(ax=ax,
                                lw=0.5,
                                label='Frontal',
                                alpha=0.25,
                                color='black')

    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)

    #plt.fill_between(filtered_df.index, -2, 2,
    #                 where=filtered_df.PeakAccel >= 0.3,
    #                 facecolor='purple', transform=trans, linewidth=1,
    #                 edgecolor='purple', antialiased=False, alpha=0.25)

    STANDING = Transverse <= -0.35

    ON_BACK = (~STANDING &
               (Frontal >= Sagittal - 0.1) &
               (Frontal >= 0.85) &
               (Sagittal <= 0.6))

    RIGHT_SIDE = (~STANDING &
                  ~ON_BACK &
                  (Sagittal + Frontal >= 0))

    LEFT_SIDE = ~(STANDING | ON_BACK | RIGHT_SIDE)

    draw_bars(data.index,
              ax=ax,
              where=STANDING,
              transform=trans,
              color=seaborn.xkcd_rgb['faded green'],
              label='Standing')

    draw_bars(data.index,
              ax=ax,
              where=ON_BACK,
              transform=trans,
              color=seaborn.xkcd_rgb['amber'],
              label='On Back')

    draw_bars(data.index,
              ax=ax,
              where=LEFT_SIDE,
              transform=trans,
              color=seaborn.xkcd_rgb['windows blue'],
              label='Left Side')

    draw_bars(data.index,
              ax=ax,
              where=RIGHT_SIDE,
              transform=trans,
              color=seaborn.xkcd_rgb['pale red'],
              label='Right Side')

    ax.set_ylim(-1.25, 1.25)

    good_labels = ['Standing', 'On Back', 'Left Side', 'Right Side']

    handles, labels = ax.get_legend_handles_labels()

    # Easier way to filter these?
    handles, labels = zip(*[(h, l) for h, l in zip(handles, labels)
                            if l in good_labels])

    legend = ax.legend(handles, labels, frameon=1, bbox_to_anchor=(1.01, 1),
                       loc=2, borderaxespad=0.0)

    frame = legend.get_frame()
    frame.set_facecolor('white')


def hr_stats(ax_1, ax_2, data):
    # Show the probability in a small bin size
    hr = data.query('HRConfidence >= 100 & HR > 20').HR

    HR_MIN = hr.min() # 60
    HR_MAX = hr.max() # 140

    bin_width = 1
    bins = numpy.arange(HR_MIN, HR_MAX + bin_width, bin_width)

    hist = hr.plot(ax=ax_1, kind='hist',
                   title='Probability of Beats per Minute', bins=bins,
                   normed=True)

    hist.yaxis.label.set_text('Probability')
    hist.yaxis.set_major_formatter(PercentFormatter)

    hist.set_xlim(xmin=HR_MIN, xmax=HR_MAX)

    # Show the degree in a larger bin size
    bin_width = 10
    bins = numpy.arange(HR_MIN, HR_MAX + bin_width, bin_width)

    hist = hr.plot(ax=ax_2, kind='hist',
                   title='Histogram of Beats per Minute', bins=bins)

    hist.set_xlim(xmin=HR_MIN, xmax=HR_MAX)
