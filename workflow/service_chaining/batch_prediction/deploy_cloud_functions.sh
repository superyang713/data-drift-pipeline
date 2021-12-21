#!/usr/bin/env bash

gcloud functions deploy batch_prediction \
--runtime python38 \
--trigger-http \
--allow-unauthenticated \
--memory=1024MB
