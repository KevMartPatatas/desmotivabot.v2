import urllib
import time
from imgNumber import leer_num_img
import requests

def descargar_imagen(src):
    numero_img = leer_num_img() # <--- Leo el numero de imagen
    ubicacion = f'img/{numero_img}.png' # <--- Carga el path

    repetir = True
    while repetir == True:
        try:
            urllib.request.urlretrieve(src, ubicacion) # <--- Descarga la imagen
            repetir = False
        except:
            time.sleep(5)
            repetir = True


def descargar_video(src):
    numero_img = leer_num_img() # <--- Leo el numero de imagen
    ubicacion = f'img/{numero_img}.mp4' # <--- Carga el path

    repetir = True
    while repetir == True:
        try:
            urllib.request.urlretrieve(src, ubicacion) # <--- Descarga la imagen
            repetir = False
        except:
            time.sleep(5)
            repetir = True
