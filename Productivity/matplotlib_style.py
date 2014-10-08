import pandas as pd
import matplotlib as mpl


def set_style():
    pd.options.display.mpl_style = 'default'
    font = {'family': 'Droid Sans',
            'weight': 'normal'}
    mpl.rc('font', **font)
    mpl.rc('figure', figsize=(8, 6))
    #mpl.rc('figure.subplot', bottom=0.2)
    mpl.rc('savefig', dpi=300)
