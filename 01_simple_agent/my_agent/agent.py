import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.cloud import secretmanager

# 1. Load the path from .env
load_dotenv()
secret_resource_name = os.getenv("SECRET_PATH")

# For Service Account JSON FILE: make sure to Assign Roles
# - Secret Manager Secret Accessor
# - Vertex AI User

# 2. Fetch the actual API Key using Secret Manager
client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(request={"name": secret_resource_name})
API_KEY = response.payload.data.decode("UTF-8")

# 3. Inject it into the environment for ADK to use
os.environ["GOOGLE_API_KEY"] = API_KEY

# 4. Initialize the Agent
root_agent = Agent(
    model='gemini-2.0-flash',  # Corrected model version
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

