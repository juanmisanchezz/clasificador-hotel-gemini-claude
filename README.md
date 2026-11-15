# Clasificador de incidencias de hotel: Qwen, Gemini ajustado y Claude

Proyecto 8 del máster de AI Engineering de thePower. *English version below.*

En el proyecto anterior entrené Qwen3-0.6B en mi Mac para clasificar las incidencias que escriben los clientes de un hotel ([repo del P7](https://github.com/juanmisanchezz/clasificador-incidencias-hotel)). Aquí hago lo mismo con modelos cerrados: entreno Gemini en Google Cloud, añado Claude sin entrenar para tener otra referencia y comparo las seis formas con los mismos 30 casos de test

Para cada mensaje el modelo tiene que devolver solo un JSON:

```json
{"categoria": "habitacion", "prioridad": "alta", "respuesta": "Lamentamos la molestia. Indíquenos su número de habitación para que recepción pueda revisarlo."}
```

Las reglas de categorías y prioridades están en [contrato.md](contrato.md), igual que en el P7.

## Las seis formas que comparo

| | Modelo | Cómo |
|---|---|---|
| 1 | Qwen3-0.6B | solo instrucciones |
| 2 | Qwen3-0.6B | instrucciones y 5 ejemplos (few-shot) |
| 3 | Qwen3-0.6B + LoRA | entrenado con los 240 ejemplos |
| 4 | Gemini 3.1 Flash-Lite base | solo instrucciones |
| 5 | Gemini 3.1 Flash-Lite ajustado | entrenado con los 240 ejemplos, solo instrucciones |
| 6 | Claude Haiku 4.5 | instrucciones y los mismos 5 ejemplos del few-shot del P7 |

Los resultados de Qwen son los del P7. No los volví a ejecutar porque no he cambiado ni los datos ni la configuración; solo los pasé otra vez por el validador de este proyecto y salen igual (6, 14 y 22).

Gemini base y ajustado llevan las mismas instrucciones ([prompts/basico.txt](prompts/basico.txt)) y la misma configuración: temperatura 0, como mucho 180 tokens y thinking `MINIMAL`. En ninguno de los seis uso JSON mode, ni arreglo la respuesta, ni vuelvo a preguntar si sale mal. Guardo cada respuesta tal cual y la corrige el mismo [validador.py](validador.py). Si algo no se puede leer como JSON, cuenta como fallo.

## Los datos

Son los mismos del P7, sin tocar: 240 de entrenamiento, 30 de validación y 30 de test (lo comprobé con `cmp`). Son inventados, no hay mensajes de clientes reales.

[convertir_gemini.py](convertir_gemini.py) los pasa al formato que pide Gemini (`systemInstruction` y `contents` con `parts`) y guarda en `datos/gemini/ids.json` qué id original tiene cada línea. El test lo convierto, pero nunca lo subí a Google: para entrenar solo usé entrenamiento y validación.

## El entrenamiento de Gemini

- Proyecto mío de Google Cloud, con un presupuesto de 10 € y alerta.
- Entrenamiento en `europe-west4` y predicciones en el endpoint `eu`.
- Modelo base `gemini-3.1-flash-lite`, 2 épocas y adaptador de tamaño 8.
- Lo lancé desde la consola web y tardó 42 minutos.

El primer trabajo lo cancelé porque lo había configurado mal; el bueno es el segundo. Los dos recibos están en [evidencias/](evidencias/) (`job-v1-cancelado.json` y `job-v2-terminado.json`), con los identificadores del trabajo, del modelo y del endpoint, y hay una captura en [capturas/5-ajuste-terminado.png](capturas/5-ajuste-terminado.png). Los identificadores que usa el código van en variables de entorno.

## Cómo está hecho

- [modelos_remotos.py](modelos_remotos.py) habla con Gemini (librería `google-genai`) y con Claude (por OpenRouter). Cada llamada devuelve el texto y los tokens que dice el proveedor.
- [evaluar.py](evaluar.py) pasa los casos por cada modelo, mide cuánto tarda cada respuesta, la corrige con el validador y lo guarda todo en `resultados/`.
- [resumir.py](resumir.py) lee esos archivos y saca la tabla: aciertos, tiempo medio, tokens medios y coste.
- Primero probé con unos pocos casos de validación para ver que todo funcionaba. El test lo pasé una sola vez al final y después no cambié nada.

## Resultados en test

Cuento un acierto cuando acierta la categoría y la prioridad a la vez.

| | JSON válido | Categoría | Prioridad | Las dos | Tiempo medio | Tokens entrada / salida | Coste por 1.000 incidencias |
|---|---|---|---|---|---|---|---|
| Qwen instrucciones | 30 | 23 | 9 | 6 | no medido | no medido | gratis (mi Mac) |
| Qwen few-shot | 30 | 22 | 18 | 14 | no medido | no medido | gratis (mi Mac) |
| Qwen LoRA | 30 | 28 | 24 | 22 | no medido | no medido | gratis (mi Mac) |
| Gemini base | 30 | 28 | 28 | 26 | 1,4 s | 274 / 57 | 0,17 $ |
| Gemini ajustado | 30 | 28 | 29 | 27 | 2,3 s | 274 / 36 | 0,13 $ |
| Claude Haiku 4.5 | 30 | 26 | 27 | 23 | 1,8 s | 748 / 60 | 1,05 $ |

En el P7 no medí tiempos ni tokens de Qwen, así que no me los invento. Qwen corría en mi MacBook Air M4 de 16 GB, Gemini en Google Cloud (Europa) y Claude a través de OpenRouter. Claude gasta más tokens de entrada porque lleva los 5 ejemplos en cada pregunta.

## Lo que ha costado

Separo lo que cuesta entrenar de lo que cuesta usar los modelos.

**Entrenar Gemini (una sola vez):** Google cobra 3 $ por millón de tokens de entrenamiento, multiplicado por las épocas. El recibo dice 75.128 tokens por época, así que 75.128 × 2 × 3 ÷ 1.000.000 son unos 0,45 $. En la facturación de Google Cloud me salen 0,42 € en total ([captura](capturas/8-facturacion-google-cloud.png)), y de eso 0,01 € es lo que gasté usando el modelo ajustado en las pruebas.

**Usarlos:** lo calculo con los tokens que devolvió cada proveedor y las tarifas oficiales, por millón de tokens:

- Gemini 3.1 Flash-Lite en Europa: 0,275 $ de entrada y 1,65 $ de salida. La [página de precios de Google](https://cloud.google.com/vertex-ai/generative-ai/pricing) dice que el modelo ajustado cobra lo mismo que el base, y la factura real lo confirma.
- Claude Haiku 4.5 en [OpenRouter](https://openrouter.ai/anthropic/claude-haiku-4.5): 1 $ de entrada y 5 $ de salida.

Con eso sale la última columna de la tabla. Incluso el más caro, Claude, cuesta alrededor de 1 $ por cada mil incidencias.

## Dónde fallan

Los dos Gemini fallan casi en los mismos casos:

- "Al grupo de la excursión nos han cargado a todos el traslado dos veces": dicen media, y es alta porque afecta a muchos clientes. Qwen LoRA también fallaba aquí.
- "¿Aceptáis pago con Bizum?" y "Urgente: ¿el parking se paga aparte?": dicen consulta, y en mis datos son facturacion. Como ya vi en el P7, aquí el modelo tiene bastante razón, porque son preguntas y no errores de cobro. El fallo es más de mis etiquetas que suyo.

La única diferencia entre los dos Gemini es "La tarjeta no abre mi habitación y es la una de la madrugada": el base dice media y el ajustado acierta con alta.

Claude se pasa con la prioridad: pone alta el ascensor averiado y la piscina sin calefacción, que con mis reglas son media. También manda a consulta cosas como pedir perchas o la factura por correo.

## Qué elegiría

Yo elegiría Gemini base. Al final, comparado con el ajustado, solo pierde un acierto completo: las categorías las hace igual y en prioridad falla solo una más. El tiempo medio de respuesta es el más bajo, y el máximo también, y el coste por cada 1.000 incidencias es muy bajo sin tener que pagar el entrenamiento.

Entrenar Gemini no ha merecido la pena con estos datos, porque solo ha sacado un acierto más. El ajustado contesta más corto y sale algo más barato de usar (0,13 $ frente a 0,17 $ por mil), pero el entrenamiento solo se amortizaría a partir de unas 13.000 incidencias.

Eso sí, 30 casos no es un gran número para comparar. Para elegir uno a largo plazo pondría muchas más incidencias y vería si sale más rentable Gemini ajustado, Gemini base o Claude.

En control gana Qwen, porque funciona en mi ordenador, los mensajes de los clientes no salen del hotel y no dependo de que otra empresa cambie precios o modelos. Pero se queda en 22 de 30 y falla prioridades que en un hotel importan, así que hoy por hoy me quedo con Gemini base.

## Qué he aprendido

- Un modelo grande sin entrenar ya hace casi todo el trabajo. Gemini base, solo con instrucciones, saca 26 de 30; Qwen necesitaba entrenar para llegar a 22.
- Entrenar un modelo cerrado es barato y rápido (0,42 € y 42 minutos), pero solo compensa si la mejora se nota.
- El coste hay que mirarlo en la factura, no solo en la cuenta. Aquí coincidían, pero es la única forma de estar seguro.
- Para comparar de forma justa hay que dejar todo fijo antes: mismos datos, mismas instrucciones, mismo validador y el test una sola vez.

## Cómo ejecutarlo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # proyecto de Google Cloud, región, endpoint del modelo ajustado y clave de OpenRouter
gcloud auth application-default login
python -m pytest        # tests del validador
python convertir_gemini.py
python evaluar.py       # cuesta dinero: llama a Gemini y a Claude
python resumir.py
```

El entrenamiento se lanza desde la consola de Google Cloud, subiendo `datos/gemini/train.jsonl` y `validacion.jsonl` a un bucket.

---

# Hotel incident classifier: Qwen, fine-tuned Gemini and Claude

Project 8 of thePower's AI Engineering master's.

In the previous project I fine-tuned Qwen3-0.6B on my Mac to classify hotel guest messages. Here I do the same with closed models: a real fine-tune of Gemini 3.1 Flash-Lite on Google Cloud, plus Claude Haiku 4.5 without training as a reference, and I compare six setups on the same 30 test cases. Same data, same instructions for Gemini base and tuned, same validator, no JSON mode and no retries.

| | Both right (of 30) | Avg. latency | Cost per 1,000 messages |
|---|---|---|---|
| Qwen instructions / few-shot / LoRA | 6 / 14 / 22 | not measured | free (local) |
| Gemini base | 26 | 1.4 s | $0.17 |
| Gemini fine-tuned | 27 | 2.3 s | $0.13 |
| Claude Haiku 4.5 | 23 | 1.8 s | $1.05 |

Fine-tuning Gemini cost €0.42 in total (about $0.45 for 75,128 tokens × 2 epochs), checked on the real Google Cloud bill. I would pick Gemini base: only one hit less than the tuned model, the fastest, very cheap and no training needed. With only 30 test cases, a one-hit difference proves nothing. Qwen wins on control because it runs locally, but it is clearly behind in quality.
