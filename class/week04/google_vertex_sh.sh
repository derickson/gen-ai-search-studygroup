source .env
gcloud auth application-default login --no-launch-browser
gcloud auth application-default set-quota-project $GOOGLE_PROJECT_NAME