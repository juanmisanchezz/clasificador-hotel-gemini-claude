import json
from modelos_remotos import preguntar_gemini, preguntar_claude
from validador import validar
import os

def evaluar (nombre, split, cuantos):
    filas = open ("datos/" + split + ".jsonl").readlines()[:cuantos]
    for fila in filas:
        ejemplo = json.loads(fila)
        if nombre == "gemini_base":
            texto, entrada, salida = preguntar_gemini(ejemplo["incidencia"], 
                                                      "gemini-3.1-flash-lite")

        elif nombre == "gemini_ajustado":
            texto, entrada, salida = preguntar_gemini(ejemplo["incidencia"], 
                                                      os.getenv("GEMINI_TUNED_ENDPOINT"))

        else:
            texto, entrada, salida = preguntar_claude(ejemplo["incidencia"])

        print (ejemplo["id"], texto)

evaluar("gemini_ajustado", "validacion", 2)
