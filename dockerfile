#specifing the docker image
FROM python:3.9-slim

#setting working directory where my app code is in.
WORKDIR /app

#copying files from project workdir to docker dir
COPY requirements.txt .
COPY key_comp/numerical_imputer.joblib .
COPY key_comp/scaler.joblib .
COPY key_comp/sepsis_model.joblib .

RUN pip install  -r requirements.txt

#copying the entire project code to the container
COPY app.py .

# Copy the model to the Docker directory
COPY key_comp /app/key_comp

#specfying the port that my fastapi is in
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
