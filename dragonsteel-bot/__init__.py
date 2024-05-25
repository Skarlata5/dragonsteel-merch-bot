import datetime
import logging
import requests
from bs4 import BeautifulSoup
import tweepy
import json
import os
import azure.functions as func

# Configuración de la API de Twitter
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')


# Crear Client en la API de Twitter
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# URL de la tienda en línea
url = 'https://www.dragonsteelbooks.com/collections/all'

def obtener_numero_de_paginas(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Encuentra el elemento que contiene el número total de páginas
        # Esto depende de la estructura HTML del sitio web
        pagination = soup.find('div', class_='pagination')
        if pagination:
            pages = pagination.find_all('a')
            return int(pages[-2].text)  # El penúltimo enlace suele ser el último número de página
    return 1  # Por defecto, si no se encuentra paginación, asumir que hay solo una página

def obtener_productos_de_pagina(url):
    response = requests.get(url)
    productos = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='product-card__details')
        for item in items:
            sold_out = buscar_sold_out_label(item)
            nombre = item.find('h3', class_='product-card__title f-family--heading f-caps--true f-space--1').text
            link = item.find_parent('div').find('a')['href']
             # Verificar si hay un precio de venta
            precio_venta = item.find('span', class_='price__number price__number--sale')
            if precio_venta:
                precio = precio_venta.text.strip()
            else:
                precio = item.find('span', class_='price__number').text.strip()
            imagen_url = item.find_parent('div').find('img')['src']
            # Comprobar si la URL de la imagen es relativa y construir la URL completa si es necesario
            if imagen_url.startswith('//'):
                imagen_url = 'https:' + imagen_url
            productos.append((nombre, precio, imagen_url, sold_out, link))
    else:
        print(f'Error al acceder a la página: {response.status_code}')
    return productos

def buscar_sold_out_label(item):
    sold_out_status = False
    sold_out_label = item.find('ul', class_='product-card__label__items o-list-bare')
    if sold_out_label and sold_out_label.find('li', class_='product-card__label product-card__label--sold label label--sold_out'):
        sold_out_status = True
    return sold_out_status

def obtener_todos_los_productos(base_url):
    productos_totales = []
    num_paginas = obtener_numero_de_paginas(base_url)
    
    for pagina in range(1, num_paginas + 1):
        url = f'{base_url}?page={pagina}'
        #print(url)
        productos = obtener_productos_de_pagina(url)
        #print(f"Hay {len(productos)} en la pagina #{pagina}")
        productos_totales.extend(productos)
        #print(f"Se han encontrado un total de {len(productos_totales)} productos")
    
    return productos_totales

def cargar_catalogo():
    if os.path.exists('catalog.json'):
        with open('catalog.json', 'r') as file:
            return json.load(file)
    else:
        return {}

def guardar_catalogo(catalogo):
    with open('catalog.json', 'w') as file:
        json.dump(catalogo, file, indent=4)
    
def subir_imagen_a_twitter(imagen_url, headers):
    # Descargar la imagen
    image_data = requests.get(imagen_url).content

    # Subir la imagen a Twitter
    response = requests.post("https://upload.twitter.com/1.1/media/upload.json", headers=headers, files={"media": image_data})

    if response.status_code == 200:
        media_id = response.json()['media_id']
        return media_id
    else:
        print(f'Error al subir imagen a Twitter: {response.status_code}')
        return None

def publicar_en_twitter(tweet, imagen_url):
    try:
        # Descargar la imagen
        image_data = requests.get(imagen_url).content
        with open('temp_image.jpg', 'wb') as handler:
            handler.write(image_data)
        
        # Subir la imagen a Twitter
        media = api.media_upload('temp_image.jpg')
        
        # Publicar el tweet con la imagen
        client.create_tweet(text=tweet, media_ids=[media.media_id])
        print(f'Tweet publicado: {tweet}')
    except tweepy.TweepyException as e:
        print(f'Error al publicar tweet: {e}')
    except Exception as e:
        print(f'Otro error ocurrió: {str(e)}')
    finally:
        if os.path.exists('temp_image.jpg'):
            os.remove('temp_image.jpg')

def verificar_status(productos):
    catalogo = cargar_catalogo()
    count = 1

    for producto in productos:
        #print(f"verificado status del producto #{count}")
        nombre, precio, imagen_url, sold_out, link = producto
        tweet_new = f'NEW: {nombre}\n PRICE: {precio}\n https://dragonsteelbooks.com{link}'
        tweet_sold_out = f'BACK IN STOCK: {nombre}\n PRICE: {precio}\n https://dragonsteelbooks.com{link}'
        tweet_back = f'SOLD OUT: {nombre}\n https://dragonsteelbooks.com{link}'

        # Verificar si el producto ya está en el catálogo
        if nombre not in catalogo:
            # Agregar el producto al catálogo
            catalogo[nombre] = {'precio': precio, 'status': 'in stock'}
            publicar_en_twitter(tweet_new, imagen_url)
        else:
            if sold_out:
                if catalogo[nombre]['status'] != 'sold out':
                    # Cambiar el estado a 'sold out' y publicar en Twitter
                    catalogo[nombre]['status'] = 'sold out'
                    publicar_en_twitter(tweet_sold_out, imagen_url)
            elif catalogo[nombre]['status'] == 'sold out':
                # Cambiar el estado a 'in stock' si estaba agotado pero ahora no lo está
                catalogo[nombre]['status'] = 'in stock'
                publicar_en_twitter(tweet_back, imagen_url)
        guardar_catalogo(catalogo)
        count += 1

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    productos = obtener_todos_los_productos(url)
    if productos:
        verificar_status(productos)

#if __name__ == '__main__':
#    productos = obtener_todos_los_productos(url)
#    if productos:
#        verificar_status(productos)