from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import joblib

app = FastAPI()


def load_model():
    num_imputer = joblib.load('numerical_imputer.joblib')
    scaler = joblib.load('scaler.joblib')
    model = joblib.load('sepsis_model.joblib')
    return num_imputer, scaler, model


def preprocess_input_data(sepsis_patient_data: dict, num_imputer, scaler):
    input_df = pd.DataFrame(sepsis_patient_data, index=[0])
    input_df = pd.DataFrame(num_imputer.transform(input_df), columns=input_df.columns)
    input_df = pd.DataFrame(scaler.transform(input_df), columns=input_df.columns)
    return input_df


def predict_sepsis_from_data(sepsis_patient_data: pd.DataFrame, model):
    prediction = model.predict(sepsis_patient_data)[0]
    return prediction


class SepsisPatientData(BaseModel):
    age: int
    plasma_glucose: int
    blood_pressure: int
    blood_work_result_1: int
    blood_work_result_2: int
    blood_work_result_3: int
    blood_work_result_4: int
    body_mass_index: int
    insurance: int


@app.get("/")
def root():
    return {"API": "Sepsis Prediction"}


@app.post("/predict")
def predict_sepsis(sepsis_patient_data: SepsisPatientData):
    num_imputer, scaler, model = load_model()

    input_df = preprocess_input_data(sepsis_patient_data.dict(), num_imputer, scaler)

    prediction = predict_sepsis_from_data(input_df, model)

    if prediction == 1:
        result = "Positive Sepsis"
    else:
        result = "Negative Sepsis"

    return {"result": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
