import json

def resumir(ruta):
    ambas = 0
    total_latencia = 0
    total_entrada = 0
    total_salida = 0

    casos = 0
    for linea in open (ruta):
        caso = json.loads(linea)
        if caso["resultado"]["categoria_correcta"] and caso["resultado"]["prioridad_correcta"]:
            ambas = ambas +1
        casos = casos + 1
        if "latencia" in caso:
            total_latencia = total_latencia + caso["latencia"]
        if "tokens_entrada" in caso:
            total_entrada = total_entrada + caso["tokens_entrada"]
        if "tokens_salida" in caso:
            total_salida = total_salida + caso["tokens_salida"]
    if total_latencia > 0:
        media = total_latencia / casos
    else:
        media = "no medido"
    if total_entrada > 0:
        media_entrada = total_entrada / casos
    else: 
        media_entrada = "no medido"
    if total_salida > 0 :
        media_salida = total_salida / casos
    else:
        media_salida = "no medido" 

    return ambas, media, media_entrada, media_salida

modelos = {
    "Qwen basico": "resultados/qwen_basico.jsonl",
    "Qwen few-shot": "resultados/qwen_fewshot.jsonl",
    "Qwen LoRA": "resultados/qwen_lora.jsonl",
    "Gemini base": "resultados/gemini_base_test.jsonl",
    "Gemini ajustado": "resultados/gemini_ajustado_test.jsonl",
    "Claude con prompt": "resultados/claude_prompt_test.jsonl"
}

tarifas = {
    "Gemini base": (0.275, 1.65),
    "Gemini ajustado": (0.275, 1.65),
    "Claude con prompt": (1.00, 5.00)
}

for modelo,ruta in modelos.items():
    aciertos, latencia, entrada, salida = resumir(ruta)

    if modelo in tarifas:
        precio_entrada, precio_salida = tarifas[modelo]
        coste_entrada = precio_entrada * entrada
        coste_salida = precio_salida * salida
        coste = (coste_entrada + coste_salida) / 1000000 * 1000
    else:
        coste = "gratis (local)" 

    print(modelo,aciertos, latencia, entrada, salida, coste)
