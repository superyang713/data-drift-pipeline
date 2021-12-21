import joblib
from io import BytesIO

import pandas as pd
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


def batch_prediction(request):
    """
    Cloud function entry point
    """
    data = request.get_json()
    data_bucket = data['bucket']
    data_blob = data['blob']

    model = load_model(MODEL_BUCEKT, MODEL_BLOB, MODEL_LOCAL_PATH)
    data = load_data(data_bucket, data_blob)
    X = data.drop(["datetime"], axis=1)
    data["prediction"] = model.predict(X)
    write_to_bigquery(data, TABLE_ID)

    response = {
        "status": "normal",
        "message": "batch prediction complete."
    }
    return jsonify(response)


def load_model(bucket_name, blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_name)
    model = joblib.load(destination_file_name)
    return model


def load_data(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    data = BytesIO(bucket.blob(blob_name).download_as_string())
    df = pd.read_csv(data)
    return df


def write_to_bigquery(data: pd.DataFrame, table_id):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("datetime", "TIMESTAMP"),
            bigquery.SchemaField("season", "INT64"),
            bigquery.SchemaField("holiday", "INT64"),
            bigquery.SchemaField("workingday", "INT64"),
            bigquery.SchemaField("temp", "FLOAT"),
            bigquery.SchemaField("atemp", "FLOAT"),
            bigquery.SchemaField("humidity", "INT64"),
            bigquery.SchemaField("windspeed", "FLOAT"),
        ],
        source_format=bigquery.SourceFormat.CSV,
    )

    load_job = client.load_table_from_dataframe(
        data, table_id, job_config=job_config)
    load_job.result()
