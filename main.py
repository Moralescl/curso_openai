from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
respuesta = cliente.chat.completions.create(
    messages= [
        {
            "role":"system",
            "content":"Eres un asistente de E-Commerce de productos sustentable, cuando te pidan productos devuelve solo el nombre sin considerar la descipcion"
        },
        {
            "role":"user",
            "content":"Liste 3 productos sustentables"
        }
    ],
    model = "gpt-4o"
)

print(respuesta.choices[0].message.content)