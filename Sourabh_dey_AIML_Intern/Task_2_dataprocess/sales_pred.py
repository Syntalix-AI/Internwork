import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



#df = pd.read_csv("Train-Set.csv")#dataframe object
#df = pd.read_csv("deputies_dataset.csv")
df = pd.read_csv("audible_uncleaned.csv")



#function for data insights
def data_insights(df):
    
    #df = pd.read_csv(d)#dataset from kaggle
    #printing first 5 rows for it
    print("FIRST 5 ROWS ARE-")
    print(df.head())
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
    print("\n")
    
    print("MAX COLUMN VALUE\n")

    print(df.columns.max())

    print("\n")

    print("MIN COLUMN VALUE\n")
    print(df.columns.min())
    print("\n")
    print("NULL VALUES\n")
    print(df.isna().sum())
    print("\n")

data_insights(df)


#for data visualization
def data_vis(df,field1,field2):
    #creating excel reading object
    #df = pd.read_csv(df)#dataset from kaggle
    #print(df[field1].value_counts())
    #print(df[field2].value_counts())
    #sns.countplot(x=field1, hue=field2, data=df)
    fig, axes = plt.subplots(2,2)

    # Plotting first subplot
    axes[0,0].set_title(f"{field1} vs {field2}")
    sns.countplot(x=field1, hue=field2, data=df, ax=axes[0,0])
    
    # Plotting second subplot
    axes[0,1].set_title(f"{field3} vs {field4}")
    sns.countplot(x=field3, hue=field4, data=df, ax=axes[0,1])

    # Plotting third subplot
    axes[1,0].set_title(f"{field5} vs {field6}")
    sns.countplot(x=field3, hue=field4, data=df, ax=axes[1,0])

    # Plotting fourth subplot
    axes[1,1].set_title(f"{field7} vs {field8}")
    sns.countplot(x=field3, hue=field4, data=df, ax=axes[1,1])
    
    # enabling the plot
    plt.tight_layout()  # Adjusting layout to prevent overlapping
    plt.show()
    plt.close()



df = df.dropna()


print("\nAFTER DROPPING THE NULL VALUES WE HAVE THE INSGIHTS AS FOLLOWS:\n")

data_insights(df)




















