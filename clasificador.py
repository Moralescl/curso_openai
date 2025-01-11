from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
modelo  = "gtp-4o"
prompt_sistema = """

"""

prompt_usuario = """

"""
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
respuesta = cliente.chat.completions.create(
    messages= [
        {
            "role":"system",
            "content":prompt_sistema
            },
        {
            "role":"user",
            "content":prompt_usuario
        }
    ],
    model = modelo,
    temperature=1,
    max_tokens=200,
    
)

print(respuesta.choices[0].message.content)