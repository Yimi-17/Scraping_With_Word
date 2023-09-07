import requests
from bs4 import BeautifulSoup
from collections import deque

#En esta lista crearemos un resgistro de los enlaces para evitar duplicidad 
enlaces_explorados = set()

def buscar_palabra(palabra,url):
    responce = requests.get(url)
    
    if responce.status_code == 200:
        #Parseamos el contenido del enlace 
        soup=BeautifulSoup(responce.text, 'html.parser')

        #Ubicamos el div deseado
        div_contenido = soup.find('div', class_='content-inner')

        #Buscamos la palabra deseada
        if div_contenido and palabra in div_contenido.text:
            print(palabra, "url encontrada:", url)
        else:
            print("Div no encontrado o palabra no encontrada en la url:", url)

    else:
        print("Error al acceder a la url", url)

#Funcion para explorar la url por niveles en sus enlaces
def explorar_enlaces(url_inicial, nivel_maximo):
    cola = deque([(url_inicial, 0)]) #Iniciamos una cola con la URL de inicio y con nivel 0
    
    while cola:
        url_actual, nivel_actual = cola.popleft()
        enlaces_explorados.add(url_actual)

        if nivel_actual<=nivel_maximo:
            responce = requests.get(url_actual)
    
            if responce.status_code == 200:
                #Parseamos el contenido del enlace 
                soup=BeautifulSoup(responce.text, 'html.parser')

                #Obtenemos todas los enlaces <a> de la url actual
                enlaces = soup.find_all('a', href=True)

                for cada_enlace in enlaces:
                    enlace_url = cada_enlace['href']

                    if enlace_url.startswith('http') and enlace_url not in enlaces_explorados:
                        cola.append((enlace_url, nivel_actual+1))
                        enlaces_explorados.add(enlace_url)

                        buscar_palabra("Juliaca", enlace_url)


#Invocamos a la funcion 
explorar_enlaces("https://www.losandes.com.pe/", 4)

#buscar_palabra("Juliaca", "https://www.losandes.com.pe/")
