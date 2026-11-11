import json

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

