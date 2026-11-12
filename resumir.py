import json

def resumir(ruta):
    ambas = 0
    for linea in open (ruta):
        caso = json.loads(linea)
        if caso["resultado"]["categoria_correcta"] and caso["resultado"]["prioridad_correcta"]:
            ambas = ambas +1
    return ambas

print(resumir("resultados/gemini_ajustado_test.jsonl"))
print(resumir("resultados/qwen_lora.jsonl"))
