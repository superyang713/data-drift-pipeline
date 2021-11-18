#!/usr/bin/env python3
from google.cloud import bigquery


PROJECT = "mightyhive-data-science-poc"
DATASET = "data_drift_demo"
TABLE_NAME = "serving"
TABLE_ID = f"{PROJECT}.{DATASET}.{TABLE_NAME}"


def handler(event, context):
    blob_name = event["name"]
    bucket_name = event["bucket"]
    uri = f"gs://{bucket_name}/{blob_name}"

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("datetime", "TIMESTAMP"),
            bigquery.SchemaField("season", "INT64"),
            bigquery.SchemaField("holiday", "INT64"),
            bigquery.SchemaField("workingday", "INT64"),
            bigquery.SchemaField("weather", "INT64"),
            bigquery.SchemaField("temp", "FLOAT"),
            bigquery.SchemaField("atemp", "FLOAT"),
            bigquery.SchemaField("humidity", "INT64"),
            bigquery.SchemaField("windspeed", "FLOAT"),
            bigquery.SchemaField("casual", "INT64"),
            bigquery.SchemaField("registered", "INT64"),
            bigquery.SchemaField("count", "INT64"),
        ],
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )

    load_job = client.load_table_from_uri(
        uri, TABLE_ID, job_config=job_config
    )
    load_job.result()

    return {"status": 1}
