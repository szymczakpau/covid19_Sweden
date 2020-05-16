import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.patches as mpatches
from matplotlib import dates
import numpy as np

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'24',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
plt.rcParams.update(params)


if __name__ == "__main__":
    poland = pd.read_csv('../data/poland_restrictions.csv')
    sweden = pd.read_csv('../data/sweden_restrictions.csv')
    poland['Date'] = poland['Date'].astype('datetime64[ns]')
    sweden['Date'] = sweden['Date'].astype('datetime64[ns]')
    poland['Event'] = poland['Event'].str.wrap(80)
    sweden['Event'] = sweden['Event'].str.wrap(80)
    date = list(poland['Date']) + list(sweden['Date'])


    sweden_levels = np.array([-2, -6, -8, -2, -3])

    poland_levels = np.array([1, 3, 7, 12, 9, 3, 1])

    fig, ax = plt.subplots(figsize=(16, 5.3), constrained_layout=True)
    ax.set_title(
        "Legal restrictions introduced by Polish and Swedish\n governments due to Coronavirus outbreak",
        size=20,
        loc='left',
        pad=50
    )

    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    xaxis = dates.date2num(date)  # Convert to maplotlib format
    hfmt = dates.DateFormatter('%m\n%d')
    ax.xaxis.set_major_formatter(hfmt)

    s_markerline, s_stemline, s_baseline = ax.stem(sweden['Date'], sweden_levels,
                                                   linefmt="C1-", basefmt="k-",
                                                   use_line_collection=True)

    p_markerline, p_stemline, p_baseline = ax.stem(poland['Date'], poland_levels,
                                                   linefmt="C3-", basefmt="k-",
                                                   use_line_collection=True)

    plt.setp(s_markerline, mec="k", mfc="w", zorder=3)
    plt.setp(p_markerline, mec="k", mfc="w", zorder=3)

    # Shift the markers to the baseline by replacing the y-data by zeros.
    s_markerline.set_ydata(np.zeros(len(sweden['Date'])))
    p_markerline.set_ydata(np.zeros(len(poland['Date'])))

    s_vert = np.array(['top', 'bottom'])[(sweden_levels > 0).astype(int)]
    for i, (d, l, r, va) in enumerate(zip(sweden['Date'], sweden_levels, sweden['Event'], s_vert)):
        if i in [0, 3]:
            ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                        textcoords="offset points", va=va, ha="right", size=12)
        elif i == 4:
            ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                        textcoords="offset points", va=va, ha="left", size=12)
        else:
            ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                        textcoords="offset points", va=va, ha="center", size=12)

    p_vert = np.array(['top', 'bottom'])[(poland_levels > 0).astype(int)]
    for i, (d, l, r, va) in enumerate(zip(poland['Date'], poland_levels, poland['Event'], p_vert)):
        if i in [2, 1]:
            ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                        textcoords="offset points", va=va, ha="right", size=12)
        elif i in [4, 5, 6]:
            ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                        textcoords="offset points", va=va, ha="left", size=12)
        else:
            ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                        textcoords="offset points", va=va, ha="center", size=12)

    ax.margins(y=0.5)
    legend_elements = [
        mpatches.Patch(color='red', label='Poland'),
        mpatches.Patch(color='orange', label='Sweden')]
    ax.legend(handles=legend_elements, loc='upper left')
    #
    # plt.savefig("../figures_static/restrictions.png",
    #             bbox_inches='tight',
    #             dpi=96
    #             )

    # plt.show()