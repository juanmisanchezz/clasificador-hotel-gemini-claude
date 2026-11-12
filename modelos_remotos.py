import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()

def cliente_gemini():
    region = os.getenv("GEMINI_SERVING_LOCATION")
    proyecto = os.getenv("GOOGLE_CLOUD_PROJECT")

    return genai.Client(vertexai=True, project=proyecto, location= region, http_options=types.HttpOptions(base_url=f"https://aiplatform.{region}.rep.googleapis.com")
)