## Enable APIs: Vertex AI, Cloud Build, Cloud Run, Artifact Registry, IAM. 

gcloud services enable \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  iam.googleapis.com
  
  
# 1. Define Variables (Optional, but helpful)
export PROJECT_ID="deployment-456920"
export SA_NAME="chatbot-runner"
export SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# 2. Create the Service Account
gcloud iam service-accounts create ${SA_NAME} \
  --project=${PROJECT_ID} \
  --display-name="Chatbot Runner Service Account"
  
## 3. Assign IAM Roles
# Assign Vertex AI User role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/aiplatform.user"

# Assign Cloud Run Admin role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/run.admin"

# Assign Storage Admin role (Warning: Broad permissions)
# Consider roles/storage.objectAdmin if only object management is needed.
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.admin"

# Assign Artifact Registry Writer role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/artifactregistry.writer"

# Assign Service Account User role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/iam.serviceAccountUser"
  
## 4. (Optional) Download a JSON Key for Local Testing
gcloud iam service-accounts keys create ./gcp-key.json \
  --iam-account=${SA_EMAIL} \
  --project=${PROJECT_ID}
 
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/gcp-key.json"



## Create the Repository Command ###export REGION="asia-southeast1"
export REPO_NAME="chatbot-repo"
export REGION="us-central1"

gcloud artifacts repositories create ${REPO_NAME} \
  --project=${PROJECT_ID} \
  --repository-format=docker \
  --location=${REGION} \
  --description="Docker repository for chatbot application"
  
  
export GEMINI_API_KEY="AIzaSyDUqetr_eWX7fpmChjN4rN6FOb6frwJ1qw"


gcloud auth configure-docker us-central1-docker.pkg.dev

docker run -p 8080:8080 -v ./app/gcp-key.json:/app/key.json -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json chatbot-app
docker run -p 8080:8080 chatbot-app