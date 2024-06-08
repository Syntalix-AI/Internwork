import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
#creating excel reading object
df = pd.read_csv("audible_uncleaned.csv") #dataset location
#print(df["Age"].max())
#function for data insights
def data_insights(df):
    
    #df = pd.read_csv(d)#dataset from kaggle
    #printing first 5 rows for it
    print("FIRST 5 ROWS ARE-")
    print(df.head)
    print("\n")

    #printing the info about the dataset
    print("Information about the dataset-")
    print(df.info())
    print("\n")


    #taking important statistical insights of the dataset
    print("Some statistics of the dataset -")
    print(df.describe())
    print("\n")


    #printing the structure of the dataset
    print("ROWS,COLUMNS")
    print(df.shape)
    print("\n")

    print("columns are -")
    print(df.columns)
    
    
    
    
#for data visualization
def data_vis(df,field1,field2):#field3,field4):
    #creating excel reading object
    #df = pd.read_csv(df)#dataset from kaggle
    print(df[field1].value_counts())
    print(df[field2].value_counts())
    #sns.countplot(x=field1, hue=field2, data=df)
    fig, axes = plt.subplots(1,2)

    # Plotting first subplot
    axes[0].set_title(f"{field1} vs {field2}")
    sns.countplot(x=field1, hue=field2, data=df, ax=axes[0])
    
    # # Plotting second subplot
    # axes[1].set_title(f"{field3} vs {field4}")
    # sns.countplot(x=field3, hue=field4, data=df, ax=axes[1])
    
    # enabling the plot
    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()
    plt.close()


print("Data insights before dropping null values")
data_insights(df)
#data_vis(df,'Survived','Pclass')
print("\n \n")

#dropping null values
df = df.dropna()

df = pd.read_csv("audible_cleaned.csv") #dataset location
print("Data insights after dropping null values")

#print(df.info())
data_insights(df)
data_vis(df,'time','ratings')
