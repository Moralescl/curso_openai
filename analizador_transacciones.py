from openai import OpenAI
from dotenv import load_dotenv
import os
import openai
import json

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4o-mini"

def carga(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            datos = archivo.read()
            return datos
    except IOError as e:
        print(f"Error es: {e}")

def guardar(nombre_archivo, contenido):
    try: 
        with open(nombre_archivo, 'w',encoding='utf-8') as archivo:
            archivo.write(contenido)
    except IOError as e:
        print(f"Error al guardar el archivo {e}")

def generar_informe(transaccion):
    print('2. Generando el informe por cada transacción de posible fraude')

    prompt_sistema = f"""
    Para la siguiente transacción, proporciona un parecer, solo si su estado es de "Posible Fraude". 
    Indica en el informe una justificación por lo cual fue identificada como un fraude.
    Transacción: {transaccion}

    ## Formato de Respuesta
    "ID Transacción": "id",
    "Tipo de Transacción": "crédito o débito",
    "Establecimiento": "nombre del establecimiento",
    "Horario": "horario de la transacción",
    "Producto": "nombre del producto",
    "Cuidad": "ciudad - estado (País)"
    "Valor": "R$XX,XX",
    "Estado": "",
    "Informe" : "Colocar No Aplicable si el estado es Aprobado"
    """
    lista_mensajes = [
        {
            'role':'system',
            'content':prompt_sistema
        }
    ]

    respuesta = cliente.chat.completions.create(
        messages=lista_mensajes,
        model= modelo
    )

    contenido  = respuesta.choices[0].message.content
    return contenido

def analizador_transacciones(lista_transacciones):
    print("1. Realizando el análisis de transacciones.")
    prompt_sistema = """
    Analiza las transacciones financieras a continuación e identifica si cada una de ellas es una "Posible Fraude" o debe ser "Aprobada". 
    Agrega un atributo "Estado" con uno de los valores: "Posible Fraude" o "Aprobado".

    Cada nueva transacción debe ser insertada dentro de la lista del JSON. 

    # Posibles indicios de fraude
    - Transacciones con valores muy discrepantes
    - Transacciones que ocurren en lugares muy distantes entre sí

    Adopta el formato de respuesta a continuación para componer tu respuesta.
    
    # Formato Salida sin '''json
    {
        "transacciones": [
            {
            "id": "id",
            "tipo": "crédito o débito",
            "establecimiento": "nombre del establecimiento",
            "horario": "horario de la transacción",
            "valor": "R$XX,XX",
            "nombre_producto": "nombre del producto",
            "localización": "ciudad - estado (País)"
            "estado": ""
            },
        ]
    } 
    """

    prompt_usuario = f"""
    Considera el CSV a continuación, donde cada línea es una transacción diferente: {lista_transacciones}. 
    Tu respuesta debe adoptar el #Formato de Respuesta (solo un json sin otros comentarios)
    """
    lista_mensajes = [
        {
            'role':'system',
            'content': prompt_sistema
        },
        {
            'role':'system',
            'content':prompt_usuario
        }
    ]

    respuesta = cliente.chat.completions.create(
        messages=lista_mensajes,
        model=modelo,
        temperature=0
    )

    contenido = respuesta.choices[0].message.content

    print(f'\nContenido\n{contenido}\n')

    json_resultado  = json.loads(contenido)
    return json_resultado

def generar_recomendacion(informe):
    print("3. Generando Recomendaciones")
    prompt_sistema = f"""
    Para la siguiente transacción, proporciona una recomendacion apropiada basada en el estado y 
    los detalles de la transacción : {informe}
    Las recomendaciones pueden ser "Notificar cliente", "Activar sector Anti-Fraude" o "Realizar Verificación Manual".
    Deben ser escritas en un formato técnico.
    Incluye también una clasificación del tipo de fraude, si es aplicable. 

    """

    lista_mensajes = [
        {
            'role':'system',
            'content': prompt_sistema
        }
    ]

    respuesta = cliente.chat.completions.create(
        messages=lista_mensajes,
        model= modelo
    )

    contenido = respuesta.choices[0].message.content

    return contenido

lista_transacciones = carga('datos/transacciones.csv')
transacciones_analizadas = analizador_transacciones(lista_transacciones)

for transaccion in transacciones_analizadas['transacciones']:
    if transaccion['estado'] == 'Posible Fraude':
        informe = generar_informe(transaccion)
        print(informe)
        recomendacion = generar_recomendacion(informe)
        id_transaccion = transaccion['id']
        nombre_producto = transaccion['nombre_producto']
        estado_transaccion = transaccion['estado']

guardar(f'datos/recomendacion-{id_transaccion}-{nombre_producto}-{estado_transaccion}.txt', recomendacion)