import json
import os
from dotenv import load_dotenv
from google import genai

filas = []

with open ("datos/gemini/train.jsonl", encoding="utf-8") as archivo:
    for linea in archivo:
        filas.append(json.loads(linea))
print(len(filas))
textos = []

for fila in filas:
    textos.append(fila["contents"][0]["parts"][0]["text"])
    textos.append(fila["contents"][1]["parts"][0]["text"])
    textos.append(fila["systemInstruction"]["parts"][0]["text"])

print (len(textos))

load_dotenv()
proyecto = os.getenv("GOOGLE_CLOUD_PROJECT")
cliente = genai.Client(vertexai=True, project=proyecto, location="global")

respuesta = cliente.models.count_tokens(model="gemini-3.1-flash-lite", contents="\n".join(textos))
print(respuesta.total_tokens)

coste = respuesta.total_tokens * 2 * 3 / 1000000


print(proyecto)
print(coste)