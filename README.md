# Chatbot GCP Pipeline

This repository contains a pipeline for deploying a chatbot application on Google Cloud Platform (GCP) with automated CI/CD integration. The project leverages GCP services to host and manage the chatbot, ensuring seamless updates through continuous integration and deployment workflows. The chatbot features a user interface built with Gradio and an API powered by FastAPI for efficient and scalable interactions.

## Features

- **Chatbot Application**: A scalable chatbot built to handle user interactions.
- **Gradio UI**: A user-friendly web interface for interacting with the chatbot, built using Gradio.
- **FastAPI Backend**: A high-performance API for handling chatbot requests, built with FastAPI.
- **GCP Integration**: Utilizes GCP services (e.g., Cloud Run, Cloud Functions, or Compute Engine) for hosting and scaling.
- **CI/CD Pipeline**: Automated deployment of the latest version using GitHub Actions.
- **Monitoring and Logging**: Integrated with GCP's monitoring tools for performance tracking.

## Prerequisites

- A Google Cloud Platform account with billing enabled.
- GCP project set up with necessary APIs enabled (e.g., Cloud Run, Cloud Build).
- GitHub account for CI/CD integration.
- Basic knowledge of Docker, Python, Gradio, FastAPI, and GCP services.
- Tools installed: `gcloud` CLI, `git`, and a code editor.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/trhieu310/chatbot-gcp-pipeline.git
   cd chatbot-gcp-pipeline
   ```

2. **Configure GCP**

   - Create a new GCP project or use an existing one.

   - Enable required APIs (e.g., Cloud Run, Cloud Build, Container Registry).

   - Authenticate `gcloud` CLI:

     ```bash
     gcloud auth login
     gcloud config set project YOUR_PROJECT_ID
     ```

3. **Set Up Environment Variables**

   - Create a `.env` file or configure environment variables for your application (e.g., API keys, database credentials).

   - Example `.env`:

     ```
     GCP_PROJECT_ID=your-project-id
     CHATBOT_API_KEY=your-api-key
     ```

4. **Build and Deploy**

   - Build the Docker image, which includes the Gradio UI and FastAPI backend:

     ```bash
     docker build -t gcr.io/YOUR_PROJECT_ID/chatbot:latest .
     ```

   - Push to Google Container Registry:

     ```bash
     docker push gcr.io/YOUR_PROJECT_ID/chatbot:latest
     ```

   - Deploy to Cloud Run (or other GCP service):

     ```bash
     gcloud run deploy chatbot \
       --image gcr.io/YOUR_PROJECT_ID/chatbot:latest \
       --region YOUR_REGION \
       --platform managed \
       --allow-unauthenticated
     ```

5. **CI/CD Configuration**

   - The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) for automatic deployment.
   - Configure GitHub Secrets for `GCP_PROJECT_ID`, `GCP_SA_KEY` (service account key JSON), and other sensitive data.
   - On each push to the `main` branch, the workflow builds, pushes, and deploys the latest version.

## Project Structure

```
chatbot-gcp-pipeline/
├── app/                    # Chatbot application code (FastAPI backend and Gradio UI)
├── Dockerfile              # Docker configuration for containerization
├── .github/workflows/      # CI/CD pipeline configuration (e.g., deploy.yml)
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies (including gradio, fastapi)
└── README.md               # This file
```

## Usage

- **Access the Gradio UI**: Open the URL provided by Cloud Run in a browser to interact with the chatbot via the Gradio interface.

- **Use the FastAPI Endpoint**: Test the chatbot API using cURL, Postman, or a frontend interface:

  ```bash
  curl https://your-chatbot-url.a.run.app/api/chat -d '{"message": "Hello"}'
  ```

- The FastAPI backend provides endpoints like `/api/chat` for programmatic access, with automatic documentation available at `/docs`.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, open an issue or contact the maintainer at \[hieunt.3199@gmail.com\].