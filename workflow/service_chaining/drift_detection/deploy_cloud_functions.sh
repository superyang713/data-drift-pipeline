#!/usr/bin/env bash

gcloud functions deploy drift_detection \
--runtime python38 \
--trigger-http \
--allow-unauthenticated \
--memory=4096MB
