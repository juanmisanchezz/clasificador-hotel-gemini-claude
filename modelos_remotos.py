import os 
from openai import OpenAI
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()

def cliente_gemini():
    region = os.getenv("GEMINI_SERVING_LOCATION")
    proyecto = os.getenv("GOOGLE_CLOUD_PROJECT")

    return genai.Client(vertexai=True, project=proyecto, location= region, http_options=types.HttpOptions(base_url=f"https://aiplatform.{region}.rep.googleapis.com"))


def preguntar_gemini(incidencia, modelo):
    cliente = cliente_gemini()
    config = types.GenerateContentConfig(system_instruction=open("prompts/basico.txt").read(),
                                          temperature=0, 
                                          max_output_tokens=180, 
                                          http_options=types.HttpOptions(extra_body={"generationConfig": {"thinkingConfig": {"thinkingLevel": "MINIMAL"}}}))
    respuesta = cliente.models.generate_content(model= modelo, contents= incidencia, config=config)
    return  respuesta.text

def cliente_claude():

    return OpenAI(base_url="https://openrouter.ai/api/v1",api_key=os.getenv("OPENROUTER_API_KEY"))

def preguntar_claude(incidencia):
    cliente = cliente_claude()
    mensajes = [{"role": "system","content":open("prompts/basico.txt").read() } , {"role": "user", "content": incidencia}]
    respuesta= cliente.chat.completions.create(model="anthropic/claude-haiku-4.5",
                                    messages=mensajes,
                                    temperature=0,
                                    max_tokens=180)
    return respuesta.choices[0].message.content