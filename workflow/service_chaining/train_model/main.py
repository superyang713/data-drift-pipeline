import joblib
from io import BytesIO

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from flask import jsonify
from google.cloud import bigquery
from google.cloud import storage


PROJECT = "mightyhive-data-science-poc"
MODEL_BUCEKT = "data-drift-detection"
MODEL_BLOB = "model.sav"
MODEL_LOCAL_PATH = "/tmp/model.sav"
DATASET = "data_drift_demo"
TABLE_NAME = "prediction"
TABLE_ID = f"{PROJECT}.{DATASET}.{TABLE_NAME}"


def train_model(request):
    """
    Cloud function entry point
    """
    data = request.get_json()
    data_blob = data['blob']
    date = data_blob.split("to")[0][:-1]

    labeled_data = load_data(date)
    X = labeled_data.drop(["count"], axis=1)
    y = labeled_data["count"]

    regressor = RandomForestRegressor(random_state=0, n_estimators=50)
    regressor.fit(X, y)

    save_model_to_gcs(
        regressor,
        MODEL_BUCEKT,
        MODEL_BLOB,
        MODEL_LOCAL_PATH)
    response = {
        "status": "normal",
        "message": "Model has been re-trained"
    }
    return jsonify(response)


def save_model_to_gcs(
    model,
    bucket_name,
    blob_name,
    destination_file_name
) -> RandomForestRegressor:
    joblib.dump(model, destination_file_name)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(destination_file_name)


def load_data(date: str):
    client = bigquery.Client()
    query = (
        f"""
        SELECT
          count,
          temp,
          atemp,
          humidity,
          windspeed,
          season,
          holiday,
          workingday,
          EXTRACT(DAYOFWEEK FROM datetime) AS weekday,
          EXTRACT(HOUR FROM datetime) AS hour,
        FROM
          `{PROJECT}.{DATASET}.bike_sharing`
        WHERE
          DATE(datetime) < "{date}"
        """
    )
    df = client.query(query).result().to_dataframe()
    return df
