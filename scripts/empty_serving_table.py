"""This script empty a table that contains serving data.
"""

from google.cloud import bigquery


PROJECT = "mightyhive-data-science-poc"
DATASET = "data_drift_demo"
TABLE_NAME = "serving"
TABLE_ID = f"{PROJECT}.{DATASET}.{TABLE_NAME}"


def main():
    empty_table(TABLE_ID)


def empty_table(table_id):
    client = bigquery.Client()

    query = (
        f"""
        TRUNCATE TABLE `{table_id}`
        """
    )
    query_job = client.query(query)
    query_job.result()

    print(f"Table {table_id} has been emptied")


if __name__ == '__main__':
    main()
