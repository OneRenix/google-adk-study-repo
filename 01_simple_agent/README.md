# My Agent Project

This project demonstrates a simple LLM agent built using Google's Agent Development Kit (ADK), leveraging the Gemini model via Vertex AI, with API key management handled securely by Google Secret Manager.

## Setup and Prerequisites

Before running the agent, ensure you have the following:

1.  **Google Cloud Account & Project:** Create your own Google Cloud account and project. **Pro Tip:** You can activate the free $300 credits for 90 days to get started.
2.  **Google Cloud Project APIs:** Enable the following APIs in your Google Cloud project:
    *   Secret Manager API
    *   Vertex AI API
3.  **Service Account:** A Google Cloud Service Account with the following roles:
    *   `Secret Manager Secret Accessor`
    *   `Vertex AI User`
    This service account will be used by the environment where your agent runs (e.g., a Compute Engine VM, GKE pod, or Cloud Function) to authenticate and access Secret Manager and Vertex AI. **Note:** While a Service Account JSON file can be used for local development, it is generally recommended to use Workload Identity (for GKE/GCE) or other credential mechanisms for production environments to avoid managing key files directly.
4.  **.env file:** Create a `.env` file in the `my_agent` directory with the following content:
    ```
    SECRET_PATH="projects/YOUR_PROJECT_NUMBER/secrets/YOUR_SECRET_NAME/versions/LATEST"
    GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID" # Get this from your Google Cloud project settings
    GOOGLE_CLOUD_LOCATION="YOUR_REGION" # Example: us-central1 - Get this from your Google Cloud project settings or choose a region for Vertex AI
    ```
    Replace `YOUR_PROJECT_NUMBER` with your Google Cloud project number and `YOUR_SECRET_NAME` with the name of the secret storing your `GOOGLE_API_KEY` in Secret Manager.
    Replace `YOUR_PROJECT_ID` with your Google Cloud Project ID and `YOUR_REGION` with the desired Google Cloud region for Vertex AI operations.
5.  **Google API Key in Secret Manager:** Store your `GOOGLE_API_KEY` as a secret in Google Secret Manager. The `SECRET_PATH` in your `.env` file should point to this secret.

## Key Design Decisions

### Why use Secret Manager over Service Account JSON for API Keys?

While a Service Account JSON file is a valid method for authentication, using Google Secret Manager to store and retrieve your `GOOGLE_API_KEY` offers significant advantages, especially for managing sensitive credentials:

*   **Enhanced Security:** Secret Manager provides a dedicated, secure, and centralized service for storing secrets. Secrets are encrypted at rest and in transit, and access is controlled through fine-grained Identity and Access Management (IAM) policies. This minimizes the risk of credentials being exposed in code repositories or configuration files.
*   **Centralized Management:** All secrets can be managed from a single console, simplifying auditing, rotation, and access control across your organization.
*   **Automated Rotation:** Secret Manager supports automated secret rotation, which is crucial for reducing the blast radius of compromised credentials and ensuring compliance with security best practices. Service Account JSON keys often require manual rotation processes, which can be cumbersome and error-prone.
*   **Auditability:** Every access to a secret in Secret Manager is logged to Cloud Audit Logs, providing a clear audit trail of who accessed what secret and when. This is essential for security monitoring and compliance.
*   **Reduced Risk of Exposure:** By fetching the API key at runtime from Secret Manager, the key is never hardcoded or persistently stored within the application's environment, reducing the attack surface.

### Why use Vertex AI Engine and Gemini Model vs. just an API Key?

Leveraging the Vertex AI platform for the Gemini model, rather than simply using a direct API key for model access, provides a robust and scalable solution with enterprise-grade features:

*   **Managed Service Benefits:** Vertex AI is a fully managed platform, meaning Google handles the underlying infrastructure, scaling, and maintenance. This allows developers to focus on building applications rather than managing complex MLOps pipelines.
*   **Scalability and Reliability:** Vertex AI automatically scales resources to meet demand, ensuring your applications remain performant even during peak loads. It offers high availability and reliability for deploying and serving models.
*   **Integrated MLOps Ecosystem:** Vertex AI provides a comprehensive suite of MLOps tools for the entire machine learning lifecycle, including data labeling, model training, evaluation, deployment, monitoring, and governance. This streamlines the development and operationalization of AI applications.
*   **Advanced Model Capabilities:** Access to the latest versions of the Gemini model with advanced features, including multimodal capabilities, specialized endpoints, and potential for fine-tuning to specific use cases. Vertex AI often provides optimized access and performance for Google's foundational models.  
*   **Enhanced Security and Compliance:** Benefits from Google Cloud's robust security infrastructure, ensuring data privacy and compliance with industry standards.
*   **Integration with Google Cloud Services:** Seamless integration with other Google Cloud services like Cloud Logging, Cloud Monitoring, BigQuery, and Cloud Storage, enabling comprehensive observability and data management for your AI applications.
*   **Agent Development Kit (ADK) Compatibility:** The ADK is designed to work efficiently with Vertex AI, providing a structured framework for building and deploying AI agents that can leverage the platform's capabilities effectively.

## How to Run

1.  **Initialize Environment:**
    ```bash
    uv init
    ```
    This command automatically creates a virtual environment for your project.
2.  **Install Dependencies:**
    ```bash
    uv add google-adk google-cloud-secret-manager
    ```
    This installs the necessary libraries for the Agent Development Kit and Google Cloud Secret Manager.
3.  **Configure API Key:** Set up your `.env` file as described in the "Setup and Prerequisites" section, pointing to your `GOOGLE_API_KEY` stored in Secret Manager.
4.  **Run the Agent:**
    *   To run the Agent with the built-in web UI of ADK for tracing, events, artifacts, and evaluations:
        ```bash
        uv run adk web
        ```
    *   To run it as a FastAPI server:
        ```bash
        uv run adk api_server
        ```
    *   To run it in CLI mode:
        ```bash
        uv run adk run
