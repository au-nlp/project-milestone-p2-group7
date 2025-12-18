from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("AZURE_ENDPOINT")
MODEL_NAME = "DeepSeek-V3-0324"
DEPLOYMENT_NAME = "DeepSeek-V3-0324"
API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url=ENDPOINT,
    api_key=API_KEY
)