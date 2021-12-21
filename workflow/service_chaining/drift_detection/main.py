import os
from tempfile import gettempdir

from flask import jsonify
from google.cloud import bigquery
from google.cloud import storage

from validation import TrainDataset
from validation import ServeDataset
from validation import Validator


BUCKET_NAME = "data-drift-detection"
STATS_BLOB_NAME = "stats.txt"
SCHEMA_BLOB_NAME = "schema.txt"

STATS_FILEPATH = f"/tmp/{STATS_BLOB_NAME}"
SCHEMA_FILEPATH = f"/tmp/{SCHEMA_BLOB_NAME}"


def drift_detection(request):
    data = request.get_json()
    uri = data['uri']

    download_train_assets()

    serve = ServeDataset.from_gcs(uri)
    train = TrainDataset.from_stats_file(
        input_path=STATS_FILEPATH,
        schema_input_path=SCHEMA_FILEPATH
    )

    validator = Validator(train, serve)
    result = validator.detect_drift()

    for info in result["driftSkewInfo"]:
        feature_name = info["path"]["step"][0]
        is_drifted = (
            info["skewMeasurements"][0]["threshold"] <
            info["skewMeasurements"][0]["value"]
        )
        if is_drifted:
            response = {
                "status": "attention",
                "message": result["driftSkewInfo"]
            }
            return jsonify(response)

    response = {
        "status": "normal",
        "message": "Everything is good"
    }

    return jsonify(response)


def download_train_assets():
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    stats = bucket.blob(STATS_BLOB_NAME)
    schema = bucket.blob(SCHEMA_BLOB_NAME)

    stats.download_to_filename(STATS_FILEPATH)
    schema.download_to_filename(SCHEMA_FILEPATH)
    return
