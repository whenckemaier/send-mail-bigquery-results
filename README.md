
# Cloud Function Send Mail BigQuery Results 

Cloud Functions that sends email based on the result of a query execution in BigQuery.


## Config

Before publishing the Cloud Function, it is necessary to inform the GCP `project-id` and insert the query that will be executed.
To configure the sending email and recipients, you must already have a mailgun license and then enter the `api key`, `domain`, `sender_email`, `receiver_emails`.
Optional: change the `subject` which is the title of the email and the `body` which is the body of the email.

For local testing, simply change the same parameters in the `test_local.py` file and then run with `pip test_local.py`.


## Deploy

To deploy the Cloud Function, simply run the file `./deploy.sh`

```bash
  gcloud functions deploy cloud-functions-name \
    --runtime python310 \
    --source . \
    --region us-east1 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point main \
    --memory 128mb \
    --timeout 60s
```