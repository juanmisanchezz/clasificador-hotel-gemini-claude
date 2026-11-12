import json
from modelos_remotos import preguntar_gemini, preguntar_claude
from validador import validar
import os
import time

def evaluar (nombre, split, cuantos):
    filas = open ("datos/" + split + ".jsonl").readlines()[:cuantos]
    archivo = open("resultados/" + nombre + "_" + split + ".jsonl", "w")
    marcador = {"json_valido": 0, "categoria_correcta": 0, "prioridad_correcta": 0,"ambas": 0}

    for fila in filas:
        ejemplo = json.loads(fila)
        inicio = time.perf_counter()
        if nombre == "gemini_base":
            texto, entrada, salida = preguntar_gemini(ejemplo["incidencia"], 
                                                      "gemini-3.1-flash-lite")

        elif nombre == "gemini_ajustado":
            texto, entrada, salida = preguntar_gemini(ejemplo["incidencia"], 
                                                      os.getenv("GEMINI_TUNED_ENDPOINT"))

        else:
            texto, entrada, salida = preguntar_claude(ejemplo["incidencia"])
        latencia = time.perf_counter()- inicio
        resultado = validar(texto, ejemplo["objetivo"])
        if resultado ["json_valido"]:
            marcador ["json_valido"] = marcador ["json_valido"] + 1
        if resultado ["categoria_correcta"]:
            marcador ["categoria_correcta"] = marcador ["categoria_correcta"] + 1
        if resultado ["prioridad_correcta"]:
             marcador ["prioridad_correcta"] = marcador ["prioridad_correcta"] +1
        if resultado ["categoria_correcta"] and resultado["prioridad_correcta"]:
            marcador["ambas"] = marcador["ambas"] + 1


        registro = {
            "id": ejemplo["id"],
            "incidencia": ejemplo["incidencia"],
            "esperado": ejemplo["objetivo"],
            "respuesta": texto,
            "resultado": resultado,
            "latencia": latencia,
            "tokens_entrada": entrada,
            "tokens_salida": salida,
        }
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
        print (ejemplo["id"], resultado, latencia)
    archivo.close()
    print(nombre, marcador)

    

evaluar("gemini_base", "test", 30)
evaluar("gemini_ajustado", "test", 30)
evaluar("claude_prompt", "test", 30)


