from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"



def carga(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            datos = archivo.read()
            return datos
    except IOError as e:
        print(f"Error es: {e}")

prompt_sistema = """
Identifique el perfil de compra para cada cliente a continuación.

El formato de salida debe ser:

cliente - describe el perfil del cliente en 3 palabras
"""

prompt_usuario = carga("datos\lista-compra-300-clientes.csv")

codificador = tiktoken.encoding_for_model(modelo)
lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens en la entrada: {numero_de_tokens}")
tokens_salida = 2048
limite_TPM_modelo = 10000

if numero_de_tokens + tokens_salida >= limite_TPM_modelo:
    modelo = "gpt-4o-mini"

print(f"Modelo elegido: {modelo}")

lista_mensajes = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

resposta = client.chat.completions.create(
    messages = lista_mensajes,
    model=modelo,
    max_tokens= tokens_salida
)

print(resposta.choices[0].message.content)