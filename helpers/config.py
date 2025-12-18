from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = "https://au803280-foundry.services.ai.azure.com/openai/v1/"
MODEL_NAME = "DeepSeek-V3-0324"
DEPLOYMENT_NAME = "DeepSeek-V3-0324"
API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url=ENDPOINT,
    api_key=API_KEY
)