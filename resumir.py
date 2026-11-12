import json

def resumir(ruta):
    ambas = 0
    total_latencia = 0
    casos = 0
    for linea in open (ruta):
        caso = json.loads(linea)
        if caso["resultado"]["categoria_correcta"] and caso["resultado"]["prioridad_correcta"]:
            ambas = ambas +1
        casos = casos + 1
        if "latencia" in caso:
            total_latencia = total_latencia + caso["latencia"]
    if total_latencia > 0:
        media = total_latencia / casos
    else:
        media = "no medido"
    return ambas, media

print(resumir("resultados/gemini_ajustado_test.jsonl"))
print(resumir("resultados/qwen_lora.jsonl"))
