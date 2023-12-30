import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time
import pandas as pd

import duckdb
import io

db = ChipmunkDb("localhost", 8091)

collections = db.collections()

df = db.collection_as_pandas("testdomain")


# resize the dataframe by copying it to more than 500mb
# this will cause the dataframe to be split into multiple chunks
# and the dataframe will be split into multiple chunksw
last_date = df.index[-1]
while df.memory_usage().sum() < 500000000:
    data_index = []
    data = []
    for i in range(0, 100000):
        last_date = last_date + pd.Timedelta(minutes=1)
        data_index.append(last_date)
        data.append({"datetime": last_date, "chart2.main:open": 1, "chart2.main:close": 1,
                                                              "chart2.main:high": 1, "chart2.main:low": 1, "chart2.main:volume": 1})

    df = pd.concat([df, pd.DataFrame(index=data_index, data=data)])



start = time.time()
db.save_as_pandas(df, "testdomain", mode="dropbefore")
end = time.time()
print("read complete dataframe with indicator again", end - start)






start = time.time()
d = db.query("SELECT * FROM testdomain LIMIT 10000", domain="chart1")
end = time.time()
print("extract only a part out of it", end - start)

