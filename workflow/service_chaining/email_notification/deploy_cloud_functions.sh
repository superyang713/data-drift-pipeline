#!/usr/bin/env bash

gcloud functions deploy email_notification \
--runtime python38 \
--trigger-http \
--allow-unauthenticated \
