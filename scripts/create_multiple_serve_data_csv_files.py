"""This script dumps serve data csv files in a sequence to a GSC bucket to mock
the real world senario.

This event is the start of the ML pipeline that will trigger a cloud function
for further actions.

"""
import time
import datetime as dt

from google.cloud import bigquery


PROJECT = "mightyhive-data-science-poc"
BUCKET = "serve-data-mock"
DATASET = "data_drift_demo"
TABLE_NAME = "bike_sharing"
TABLE_ID = f"{PROJECT}.{DATASET}.{TABLE_NAME}"


def main():
    interval = dt.timedelta(days=28)
    start = dt.date(2011, 1, 29)

    for i in range(1, 10):
        end = start + interval
        dump_serve_data(start, end, BUCKET)

        start = start + interval + dt.timedelta(days=1)
        print("Waiting for new serve data")
        time.sleep(2)


def dump_serve_data(start: dt.date, end: dt.date, bucket: str):
    client = bigquery.Client()
    blob_name = f"{start}_to_{end}"

    query = (
        f"""
        EXPORT DATA OPTIONS(
            uri='gs://{bucket}/{blob_name}*.csv',
            format='CSV',
            overwrite=true,
            header=true
        ) AS

        SELECT
          *
        FROM
          `{PROJECT}.{DATASET}.bike_sharing`
        WHERE
          DATE(datetime) BETWEEN "{start}" and "{end}"
        """
    )
    query_job = client.query(query)
    query_job.result()


if __name__ == '__main__':
    main()
