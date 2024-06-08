import numpy as np
import pandas as pd

df = pd.read_csv("deputies_dataset.csv")

col = list(df.columns)

print(col)


col_name = input("Enter the column name whose Outlier you want to check among the above columns: ")

data = df[col_name]


def outliers_detect(data):
    outliers = []
    thres = 3
    mean = np.mean(data)
    std = np.std(data)
    #col = df["Weight"]
    #for i in col:
    for i in data:
        z_val = (i - mean)/std
        if (np.abs(z_val)>thres):
            outliers.append(i)
    return outliers

print(outliers_detect(data))
            
        
