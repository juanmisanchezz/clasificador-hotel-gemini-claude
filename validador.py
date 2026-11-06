import json



def validar (texto, esperado):
    out = {
        "json_valido": False,
        "categoria_correcta": False,
        "prioridad_correcta": False,
    }
    try:
        datos = json.loads(texto)
        if not isinstance(datos, dict):
            return out
        out["json_valido"] = True
        if "categoria" in datos and datos["categoria"] == esperado["categoria"]:
            out["categoria_correcta"] = True
        if "prioridad" in datos and datos["prioridad"] == esperado["prioridad"]:
            out["prioridad_correcta"] = True
    except (json.JSONDecodeError,TypeError):
        return out
    return out

