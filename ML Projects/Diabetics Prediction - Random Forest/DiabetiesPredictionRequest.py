from pydantic import BaseModel

class DiabetiesPredictionRequest(BaseModel):
    Pregnancies:int  
    Glucose:int  
    BloodPressure:float
    SkinThickness:int  
    Insulin:float
    BMI:float
    DiabetesPedigreeFunction:float
    Age:int
