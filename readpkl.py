import pickle
import pandas as pd
from scipy.io import loadmat
import numpy as np

with open("nsd_stim_info_merged.pkl", "rb") as f:
    df = pickle.load(f, encoding="latin1")

print(df.head())

data = loadmat("nsd_expdesign.mat")
print("Keys in MAT file:", data.keys())
print(data["subjectim"])

for key in data.keys():
    if isinstance(data[key], np.ndarray):
        print(f"{key}: {type(data[key])}, shape: {data[key].shape if hasattr(data[key], 'shape') else 'N/A'}")
        df1 = pd.DataFrame(data[key])
        print(key, df1.head)

