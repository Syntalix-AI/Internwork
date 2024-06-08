import pandas as pd

print("\nUNCLEANED DATASET\n")
df2 = pd.read_csv("audible_uncleaned.csv")
print(df2.head())

#df = list(df2.columns)
#print(df2[["author","narrator","time","stars"]])


print("\n\nCLEANED DATASET\n")
df1 = pd.read_csv("audible_cleaned.csv")
print(df1.head())
