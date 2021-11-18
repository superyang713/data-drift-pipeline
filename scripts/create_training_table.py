"""This script creates a table that contains training data.
"""

from google.cloud import bigquery


PROJECT = "mightyhive-data-science-poc"
DATASET = "data_drift_demo"
TABLE_NAME = "training"
TABLE_ID = f"{PROJECT}.{DATASET}.{TABLE_NAME}"


def main():
    start = "2011-01-01"
    end = "2011-01-28"
    create_training_table(start, end)


def create_training_table(start: str, end: str):
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(destination=TABLE_ID)

    query = (
        f"""
        SELECT
          *
        FROM
          `{PROJECT}.{DATASET}.bike_sharing`
        WHERE
          DATE(datetime) BETWEEN "{start}" and "{end}"
        """
    )
    query_job = client.query(query, job_config=job_config)
    query_job.result()

    print("Query results loaded to the table {}".format(TABLE_ID))



if __name__ == '__main__':
    create_training_table()
