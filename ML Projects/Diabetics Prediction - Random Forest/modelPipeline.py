import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split,cross_validate,StratifiedKFold
from sklearn.pipeline import Pipeline
import time
from sklearn.metrics import precision_score,recall_score,accuracy_score,roc_auc_score,f1_score
import joblib,os

path = r"E:\\Veena\\Certificate-Program-in-AIML-IIT-Patna\\ML Projects\\Diabetics Prediction - Random Forest\\DiabetiesPredictionModel.pkl"


MODELS ={
    'Logistic Regression':LogisticRegression(max_iter=1000,class_weight='balanced',random_state=42,),
    'Decision Tree':DecisionTreeClassifier(max_depth=5,class_weight='balanced',random_state=42),
    'Random Forest':RandomForestClassifier(n_estimators=1000,class_weight='balanced',random_state=42,n_jobs=-1)
}

COLUMNS = [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age"
        ]

numCols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
catCols=[]

#Here, the numeriacl scaling is not required, since it doesnot have any effect on decision trees. This is used only for my demo purpose.
def definePreprocessor():
    PREPROCESSOR= ColumnTransformer(
        [
            ('num',StandardScaler(),numCols),
            ('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),catCols)
        ]
    )
    return PREPROCESSOR

def finalisingBestModel(mlPipeline,xTrain,yTrain,xTest,yTest):

    bestModel = mlPipeline.fit(xTrain,yTrain)

    yPred = bestModel.predict(xTest)
    
    print(f"Final Model:{mlPipeline.named_steps['model']}");
    print(f"Accuracy: {accuracy_score(yTest,yPred): .2f}")
    print(f"Precision: {precision_score(yTest,yPred): .2f}")
    print(f"Recall: {recall_score(yTest,yPred): .2f}")
    print(f"F1 score : {f1_score(yTest,yPred): .2f}")
    print(f"ROC AUC Score: {roc_auc_score(yTest,yPred): .2f}")

    

    if os.path.exists(path):
        os.remove(path)
    joblib.dump(bestModel,path)

def load_model(path):
    if os.path.exists(path):
        return joblib.load(path)
    else:
        print(f"Model not found: {path}")
        return None    

def predictDiabeties(verbose=True):
    #loading the model.
    model = load_model(path)

    if model is not None:
        inputData=[[2, 120, 70, 25, 80, 28.5, 0.259, 35]]

        inputDataDf = pd.DataFrame(inputData, columns=COLUMNS)
        if verbose:
            print(f"inputDataDf: {inputDataDf}")

        predictionResult = model.predict(inputDataDf)
        if predictionResult[0] == 0:
            print("The person is Not Diabetic")
        elif(predictionResult[0] == 1):
            print("The person is Diabetic")



def mlFlow(x,y,verbose=True):
    print("----SPLITTING THE DATA INTO TEST AND TRAIN SETS----")
    xTrain,xTest,yTrain,yTest = train_test_split(x,y,test_size=0.3,random_state=42,stratify=y)

    if verbose:
        print(f"Train samples : {len(xTrain)} samples | Diabeties Rate: {yTrain.mean():.2%}")
        print(f"Test samples : {len(xTest)} samples | Diabeties Rate: {yTest.mean():.2%}")

    decidingFactor=[]
    exhaustiveResults={}
    modelPipeLines = {}

    preprocessor = definePreprocessor()

    for name,model in MODELS.items():
        mlPipeline = Pipeline([
            ('Preprocessor',preprocessor),
            ('model',model)
        ])

        modelPipeLines[name] = mlPipeline

        t0=time.time()
        print("----TRAINING THE MODEL----")
        print(f'MODEL NAME: {name}')
        mlPipeline.fit(xTrain,yTrain)
        elapsed = time.time() - t0

        yPred = mlPipeline.predict(xTrain)
        crossVal = StratifiedKFold(n_splits=5,shuffle=True,random_state=42)

        scoring = {"accuracy": "accuracy",
                   "precision": "precision",
                   "recall": "recall",
                   "f1": "f1",
                   "roc_auc": "roc_auc"
        }


        crossValidationScore = cross_validate(mlPipeline,xTrain,yTrain,cv=crossVal,scoring=scoring)

        exhaustiveResults[name] = {
            'Accuracy': crossValidationScore['test_accuracy'].mean().round(2),
            'Precision':crossValidationScore['test_precision'].mean().round(2),
            'Recall':crossValidationScore['test_recall'].mean().round(2),
            'F1':crossValidationScore['test_f1'].mean().round(2),
            'ROC AUC Score':crossValidationScore['test_roc_auc'].mean().round(2),
            'Training Time':round(elapsed,3)
            }
    print(exhaustiveResults)    
    resultsDF = pd.DataFrame(exhaustiveResults)  

    if verbose:
        print(resultsDF.to_string(index=True))

    print("----DECIDING THE BEST MODEL BASED ON METRICS----")

    bestModel = max(exhaustiveResults,
                    key=lambda m: exhaustiveResults[m]['ROC AUC Score'])
    if verbose:
        print(f"----THE BEST MODEL IS :::: {bestModel}----")
        print(f"----THE BEST MODEL's PIPELINE :::: {modelPipeLines[bestModel]}----")

    finalisingBestModel(modelPipeLines[bestModel],xTrain,yTrain,xTest,yTest)  




      
        


        









