"""This cloud function is triggered by GCS google.storage.object.finalize event.
When an object is successfully stored in specified GCS bucket, this function
will run.

The function passes the object uri to the specified workflow, and invoke it to
initialize the pipeline.
"""
import time
import json

from google.cloud.workflows_v1beta import WorkflowsClient
from google.cloud.workflows.executions_v1beta import ExecutionsClient
from google.cloud.workflows.executions_v1beta.types import executions
from google.cloud.workflows.executions_v1beta.types import Execution


PROJECT = "mightyhive-data-science-poc"
LOCATION = "us-central1"
WORKFLOW = "data-drift-pipeline"


def invoke_workflow(event, context):
    blob_name = event["name"]
    bucket_name = event["bucket"]
    uri = f"gs://{bucket_name}/{blob_name}"

    # Set up API clients.
    execution_client = ExecutionsClient()
    workflows_client = WorkflowsClient()

    # Set up arguments passed to workflow
    arguments = {"uri": uri, "bucket": bucket_name, "blob": blob_name}
    execution = Execution(argument=json.dumps(arguments))

    # Construct the fully qualified location path.
    parent = workflows_client.workflow_path(PROJECT, LOCATION, WORKFLOW)

    # Execute the workflow.
    execution_client.create_execution(
        parent=parent,
        execution=execution
    )
    return
