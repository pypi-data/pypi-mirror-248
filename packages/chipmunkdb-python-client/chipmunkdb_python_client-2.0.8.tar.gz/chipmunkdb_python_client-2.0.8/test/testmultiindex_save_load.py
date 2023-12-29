import sys
sys.path.insert(0,'..')
from chipmunkdb.ChipmunkDb import ChipmunkDb
import time


db = ChipmunkDb("localhost", 8091)

db.save_collection("prices_df")
