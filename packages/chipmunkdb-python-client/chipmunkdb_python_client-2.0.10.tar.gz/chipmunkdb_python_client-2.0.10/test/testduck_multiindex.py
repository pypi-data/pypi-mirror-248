import numpy as np
import pandas as pd

import duckdb
import io

from chipmunkdb.ChipmunkDb import ChipmunkDb

category_idx = pd.Index(['A', 'B'])
date_idx = pd.date_range('2018-01', '2018-02', freq='MS')
idx = pd.MultiIndex.from_product([category_idx, date_idx], names=['category', 'date'])

series = pd.Series(np.random.randn(len(category_idx) * len(date_idx)), index=idx)


df = pd.DataFrame(series)

cdb = ChipmunkDb("localhost", 8091)

#cdb.save_as_pandas(df, "test3")
#cdb.save_collection("test3")

df2 = cdb.collection_as_pandas("test3")

print(df2)

