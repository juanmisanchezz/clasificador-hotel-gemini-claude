import json


with open("prompts/basico.txt", encoding="utf-8") as archivo:
    instrucciones = archivo.read()

def traducir(fila):
    return {
        "systemInstruction": {"parts": [{"text": instrucciones}]},
        "contents": [
        {"role": "user",  "parts": [{"text": fila["incidencia"]}]},
        {"role": "model", "parts": [{"text": json.dumps(fila["objetivo"], ensure_ascii=False)}]}
  ]
}
relacion = {}

for nombre in ["train", "validacion", "test"]:
    filas = []
    ids = []

    with open(f"datos/{nombre}.jsonl", encoding="utf-8") as archivo:
        for linea in archivo:
            filas.append(json.loads(linea))


    with open (f"datos/gemini/{nombre}.jsonl", "w", encoding="utf-8") as salida:
        for fila in filas:
            traducida = traducir(fila)
            salida.write(json.dumps(traducida, ensure_ascii=False) + "\n")
            ids.append(fila["id"])

    print(nombre, len(filas))
    relacion[nombre] = ids
with open("datos/gemini/ids.json", "w", encoding="utf-8") as salida:
    json.dump(relacion, salida, ensure_ascii=False, indent=2)
