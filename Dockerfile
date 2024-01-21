FROM python:3.9-slim

ENV PYTHONUNBUFFERED=TRUE

RUN pip --no-cache-dir install pipenv

# equivalent to the cd command in Linux
WORKDIR /app

# copy to app folder
COPY ["Pipfile", "Pipfile.lock", "./"]

# Install dependencies and clean cache
RUN pipenv install --deploy --system && \
rm -rf /root/.cache

# Copy the predict_model.py into the src/models directory inside the container
COPY ["src/models/predict_model.py", "./src/models/"]

# Copy the random_forest_model.joblib into the models directory inside the container
COPY ["models/xgb_taxi_trip.json", "./models/"]

# port our application will use
EXPOSE 9696

# Run Gunicorn with the Flask application
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "src.models.predict_model:app"]
