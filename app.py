from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/predict-sepsis")
def predict_sepsis(patientid: str, age: int, plasma_glucose: int, Blood_Pressure: int, Blood_Work_Result_1: int,  Blood_Work_Result_2: int, Blood_Work_Result_3: int, Blood_Work_Result_4: int, Body_mass_index: int, Insurance: str ):
    # Load the random forest classifier
    rf_model = RandomForestClassifier(max_depth=15, max_features=5, random_state=42)

    # Load the patient's data
    patient_data = {"patient id": patientid, "age": age, "plasma glucose": plasma_glucose, "Blood Pressure": Blood_Pressure, "Blood Work Result 1": Blood_Work_Result_1, "Blood Work Result 2": Blood_Work_Result_2, "Blood Work Result 3": Blood_Work_Result_3, "Blood Work Result 4": Blood_Work_Result_4, "Body mass index": Body_mass_index, "Insurance": Insurance}

    # Convert the insurance status to a number
    if Insurance == "Yes":
        Insurance = 1
    else:
        Insurance = 0

    # Predict whether or not the patient has sepsis
    prediction = rf_model.predict(patient_data)

    # Return the prediction
    return {"prediction": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
