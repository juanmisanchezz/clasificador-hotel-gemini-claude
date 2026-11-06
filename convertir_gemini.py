import json


with open("prompts/basico.txt", encoding="utf-8") as archivo:
    instrucciones = archivo.read()


filas = []
with open("datos/train.jsonl", encoding="utf-8") as archivo:
   for linea in archivo:
      filas.append(json.loads(linea))

def traducir(fila):
    return {
        "systemInstruction": {"parts": [{"text": instrucciones}]},
        "contents": [
        {"role": "user",  "parts": [{"text": fila["incidencia"]}]},
        {"role": "model", "parts": [{"text": json.dumps(fila["objetivo"], ensure_ascii=False)}]}
  ]
}
with open ("datos/gemini/train.jsonl", "w", encoding="utf-8") as salida:
    for fila in filas:
        traducida = traducir(fila)
        salida.write(json.dumps(traducida, ensure_ascii=False) + "\n")
