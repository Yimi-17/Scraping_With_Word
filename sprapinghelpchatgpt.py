import requests
from bs4 import BeautifulSoup
from collections import deque

# En esta lista crearemos un registro de los enlaces para evitar duplicidad
enlaces_explorados = set()

def buscar_palabra(palabra, url):
    # Comprobamos si ya hemos explorado esta URL para evitar duplicados
    if url in enlaces_explorados:
        return

    # Agregamos la URL actual al conjunto de enlaces explorados
    enlaces_explorados.add(url)

    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Parseamos el contenido del enlace
            soup = BeautifulSoup(response.text, 'html.parser')

            # Ubicamos el div deseado
            div_contenido = soup.find('div', class_='content-inner')

            # Verificamos si se encontró el div
            if div_contenido:
                # Buscamos la palabra deseada dentro del div
                if palabra in div_contenido.text:
                    print(palabra, "encontrada en la URL:", url)
            else:
                print("No se encontró el div 'content-inner' en la URL:", url)
        else:
            print("Error al acceder a la URL", url)

    except Exception as e:
        print("Error al procesar la URL", url, ":", str(e))

# Invocamos a la función
buscar_palabra("Juliaca", "https://www.losandes.com.pe/")
