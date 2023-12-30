import arcticdb
import pandas as pd
import numpy as np

from fx_pairs import prices as px


def run(
        library: arcticdb.library.Library,
        start_date,
        end_date,
        config,
        resolution,
        diagnostics=None,
    ):

    diagnostics = {} if diagnostics is None else diagnostics

    mid: pd.DataFrame = library.read(px.CLOSE_MID, date_range=(start_date, end_date)).data

    long_w = mid.ewm(halflife=config.get('long_halflife', 120))
    short_w = mid.ewm(halflife=config.get('short_halflife', 63))

    vol = mid.diff().ewm(halflife=20).std()

    vol_scalar = 1/vol

    lr_mean = long_w.mean()
    sr_mean = short_w.mean()

    spread = lr_mean - sr_mean
    lr_sr_spread = (spread).ewm(halflife=30)
    mean_spread = lr_sr_spread.mean()
    std_spread = lr_sr_spread.std()

    diagnostics.update({
        'SR.MEAN': sr_mean,
        'LR.MEAN': lr_mean,
        'SR.LR.SPREAD': spread,
        '20D.VOL': vol,
    })

    positions = pd.DataFrame(0, index=mean_spread.index, columns=[mean_spread.name])

    positions[(lr_mean - sr_mean).abs() > (1.5 * std_spread)] = np.sign(spread) * -1

    return positions, diagnostics
