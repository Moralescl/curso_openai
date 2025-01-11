import tiktoken

modelo = "gpt-4o"
codificador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificador.encode(
"""
Eres un categorizador de productos.
        Debes asumir las categorías presentes en la lista a continuación.

        # Lista de Categorías Válidas
        1.Cat 1
        2.Cat 2
        3.Cat 3

        # Formato de Salida
        Producto: Nombre del Producto
        Categoría: presenta la categoría del producto

        # Ejemplo de Salida
        Producto: Cepillo eléctrico con recarga solar
        Categoría: Electrónicos Verdes
"""
)

print("modelo: " + modelo)
print("lista tokens: ", lista_tokens)
print("Número de tokens:", len(lista_tokens))

print(f"Costo para el modelo: {modelo} es de {(2.5*(len(lista_tokens)/1000000))}")

modelo = "gpt-4o-mini"

print("modelo: " + modelo)
print("lista tokens: ", lista_tokens)
print("Número de tokens:", len(lista_tokens))

print(f"Costo para el modelo: {modelo} es de {(0.15*(len(lista_tokens)/1000000))}")