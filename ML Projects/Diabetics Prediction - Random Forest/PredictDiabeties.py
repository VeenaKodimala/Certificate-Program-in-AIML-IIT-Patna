import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

import modelPipeline


def loadDataset(verbose=True):
    # LOAD DATASET
    path = "E:\\Veena\\Certificate-Program-in-AIML-IIT-Patna\\ML Projects\\DataSets\\diabetes.csv"
    diabetiesDF = pd.read_csv(path)
    if verbose:
        print(diabetiesDF.head(5))
        print(diabetiesDF.columns.tolist())
    return diabetiesDF

def dataStats(df):
    print("----TOTAL NO.OF ENTRIES PRESENT IN DATA----")
    print(len(df))
    print("----SHAPE OF THE DATASET----")
    print(df.shape)
    print("----INFO OF DATA----")
    print(df.info())
    print("----DESCRIPTION OF DATA----")
    print(df.describe())
    print("----TOTAL NULL VALUES IN DATA----")
    print(df.isna().sum().sum())





if __name__ == "__main__":
    print("--------LOADING THE DATASET--------")
    df = loadDataset()
    if(not df.empty):
        print("----DATA LOADED SUCCESSFULLY-----")

        print("----CHECKING THE STATISTICS OF DATA----")
        dataStats(df=df)

        print("----SPLITTING THE FEATURES AND TARGET OF DATA----")
        x = df.drop(['Outcome'],axis=1)
        y = df['Outcome']
        print(x)
        print(y)

        print("----FINDING THE BEST ML ALGORITHM----")
        modelPipeline.mlFlow(x,y,False)

        modelPipeline.predictDiabeties(False)


        













    

