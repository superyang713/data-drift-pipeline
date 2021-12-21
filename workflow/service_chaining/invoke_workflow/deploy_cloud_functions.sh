#!/usr/bin/env bash

gcloud functions deploy invoke_workflow \
--runtime python38 \
--trigger-resource gs://serve-data-mock \
--trigger-event google.storage.object.finalize
