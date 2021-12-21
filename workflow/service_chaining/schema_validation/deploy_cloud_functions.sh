#!/usr/bin/env bash

gcloud functions deploy schema_validation \
--runtime python38 \
--trigger-http \
--allow-unauthenticated \
--memory=4096MB
