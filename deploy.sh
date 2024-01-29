gcloud functions deploy sre-global-send-mail-daily-usage-apis_temp \
    --runtime python310 \
    --source . \
    --region us-east1 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point main \
    --memory 128mb \
    --timeout 60s