from datetime import datetime
import pandas as pd

# from metrapy.defaults import defaults
import pytz

def get_candles_df(candles, timezone):
    _candles = pd.DataFrame(
        candles,
        # columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'tick_volume', 'spread', 'real_volume']
    )

    _candles["Datetime"] = _candles["time"].map(
        lambda x: datetime.fromtimestamp(x, timezone or pytz.utc)
    )

    _candles = _candles.set_index("Datetime")

    return _candles


def filter_props(obj, keys):
    t = {}
    for key in keys:
        t[key] = obj[key]
    return t
