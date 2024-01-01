from hqm.tools.scales import scales as scl

import os
import pandas            as pnd
import utils_noroot      as utnr
import matplotlib.pyplot as plt
#-------------------------------
def plot_df(df, trig):
    df = df[df.trig == trig]
    ax = None
    for proc, df_p in df.groupby('kind'):
        ax=df_p.plot(x='year', y='val', yerr='err', ax=ax, label=proc)

    os.makedirs('tests/scales/', exist_ok=True)

    plt_path = f'tests/scales/{trig}.png'
    plt.savefig(plt_path)
    plt.close('all')
#-------------------------------
def test_simple():
    df = pnd.DataFrame(columns=['year', 'trig', 'kind', 'val', 'err'])
    for year in ['2011', '2012', '2015', '2016', '2017', '2018']:
        for trig in ['ETOS', 'GTIS']:
            for kind in ['bpks', 'bdks', 'bsph', 'bpk1', 'bpk2']:
                obj      = scl(dset=year, trig=trig, kind=kind)
                val, err = obj.get_scale()

                df = utnr.add_row_to_df(df, [year, trig, kind, val, err])

    plot_df(df, 'ETOS')
    plot_df(df, 'GTIS')
#-------------------------------
if __name__ == '__main__':
    test_simple()

