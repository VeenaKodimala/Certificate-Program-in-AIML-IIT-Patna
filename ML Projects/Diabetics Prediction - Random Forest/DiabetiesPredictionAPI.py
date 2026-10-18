import os
import pandas as pd
import joblib

from fastapi import FastAPI, HTTPException
import uvicorn

from DiabetiesPredictionRequest import DiabetiesPredictionRequest
from modelPipeline import COLUMNS

MODEL_PATH = r"E:\Veena\Certificate-Program-in-AIML-IIT-Patna\ML Projects\Diabetics Prediction - Random Forest\DiabetiesPredictionModel.pkl"


def load_model(path):
    if os.path.exists(path):
        model = joblib.load(path)
        print("Model loaded successfully.")
        return model
    else:
        print(f"Model not found: {path}")
        return None


def create_app():
    model = load_model(MODEL_PATH)
    api = FastAPI()

    @api.get("/")
    def root():
        return {"message": "Welcome to Diabeties Prediction System."}

    @api.get("/{name}")
    def welcome(name: str):
        return {"message": f"Hi {name}, Welcome to Diabeties Prediction System."}

    @api.post("/predict")
    def predictDiabeties(inputData: DiabetiesPredictionRequest):
        if model is None:
            raise HTTPException(status_code=500, detail="Model file is missing.")

        data = inputData.model_dump()
        print(f"INPUT DATA FOR DIABETIES PREDITION::: {data}")

        inputDF = pd.DataFrame(
            [[
                data['Pregnancies'],
                data['Glucose'],
                data['BloodPressure'],
                data['SkinThickness'],
                data['Insulin'],
                data['BMI'],
                data['DiabetesPedigreeFunction'],
                data['Age']
            ]],
            columns=COLUMNS
        )

        prediction = model.predict(inputDF)
        if prediction[0] == 1:
            return {"prediction": "The person is likely to have diabetes."}
        else:
            return {"prediction": "The person is not likely to have diabetes."}

    return api


app = create_app()

if __name__ == "__main__":
    uvicorn.run("APIBuilding:app", host="127.0.0.1", port=8000, reload=True)

