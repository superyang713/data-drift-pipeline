#!/usr/bin/env bash

gcloud functions deploy train_model \
--runtime python38 \
--trigger-http \
--allow-unauthenticated \
--memory=4096MB
