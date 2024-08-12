import os
from pathlib import Path
basepath = Path(__file__).resolve().parent
watchlistfile = basepath.joinpath("watchlist.json")
if os.path.exists(watchlistfile):
    print("file found")