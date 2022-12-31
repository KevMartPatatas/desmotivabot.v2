from PIL import Image, ImageDraw, ImageFont
import textwrap
from imgNumber import leer_num_img
from moviepy.editor import *

fuente_principal = ImageFont.truetype('recursos/fuentes/FreeSerif.ttf', 34)
fuente_secundaria = ImageFont.truetype('recursos/fuentes/EkMukta-Medium.ttf', 18)

def redimensionar_video():
    num_img = str(leer_num_img()) # <--- Llamo a la funcion para leer el numero de imagen
    video = VideoFileClip(f'img/{num_img}.mp4') # <--- Abre el video

    video = video.resize(width = 650 - 66)
    ancho_nuevo, new_height_video = video.size

    return new_height_video, video # <--- Retorno el nuevo alto de la imagen


def crear_marco_video(texto_principal, texto_secundario):
    num_img = str(leer_num_img()) # <--- Llamo a la funcion para leer el numero de imagen
    new_height_video, video = redimensionar_video()
    img_baner = Image.open('recursos/baner.png')

    ancho_imagen_marco = 650
    alto_img_marco = new_height_video + 50
    ancho_img_baner = img_baner.size[0]

    marco = Image.new('RGB', (ancho_imagen_marco, alto_img_marco))

    coordenada_final_rectangulo_x = ancho_imagen_marco - 31
    coordenada_final_rectangulo_y = new_height_video + 35 # <--- Los otros 4 pixeles son porque en la imagen existe una separacion de 2 pixeles en cada lado

    coordenada_img_baner_x = ((ancho_imagen_marco - ancho_img_baner)/2) # <--- Esta coordenada es para posicionar al baner en el centro del marco
    coordenada_img_baner_y = coordenada_final_rectangulo_y - 7 # <--- Esta coordenada es para posicionar al baner en el baner, 7 pxeles abajo del rectangulo blanco

    a = ImageDraw.ImageDraw(marco) #<--- La variable a es solo una variable auxiliar, no se me pudo ocurrir otro nombre XD
    a.rectangle(((30, 30), (coordenada_final_rectangulo_x, coordenada_final_rectangulo_y)), fill = None, outline = 'white', width = 1) # <--- Dibujo el rectangulo blnaco

    # marco.paste(img_baner, (int(coordenada_img_baner_x), int(coordenada_img_baner_y)))

    alto_img_principal = crear_texto_principal(texto_principal, ancho_imagen_marco)
    alto_img_secundario = crear_texto_secundario(texto_secundario, ancho_imagen_marco)
    crear_imagen_final(alto_img_principal, alto_img_secundario, alto_img_marco, video, coordenada_img_baner_x, coordenada_img_baner_y, marco)

    marco.save(f'marcos/{num_img}.png')


def crear_texto_principal(texto_principal, ancho_imagen_marco):
    alto_img = 0
    num_img = str(leer_num_img()) # <--- Llamo a la funcion para leer el numero de imagen

    lines = textwrap.wrap(texto_principal, width = 43) # <--- Probar a modificar esto
    for line in lines:
        line_width, line_height = fuente_principal.getsize(line)
        alto_img += line_height

    img_text_principal = Image.new('RGB', (ancho_imagen_marco, alto_img))
    dibujo_texto_principal = ImageDraw.Draw(img_text_principal)
    y_text = 0

    alto_img = 0
    lines = textwrap.wrap(texto_principal, width = 43)
    for line in lines:
        line_width, line_height = fuente_principal.getsize(line)
        dibujo_texto_principal.text(((ancho_imagen_marco - line_width) / 2, y_text), line, font=fuente_principal, fill = 'white')
        alto_img += line_height
        y_text += line_height

    img_text_principal.save(f'img_texts/principal/{num_img}.png')
    
    return alto_img


def crear_texto_secundario(texto_secundario, ancho_imagen_marco):
    alto_img = 0
    num_img = str(leer_num_img()) # <--- Llamo a la funcion para leer el numero de imagen

    lines = textwrap.wrap(texto_secundario, width = 87) # <--- Probar a modificar esto
    for line in lines:
        line_width, line_height = fuente_secundaria.getsize(line)
        alto_img += line_height
    
    img_text_secundario = Image.new('RGB', (ancho_imagen_marco, alto_img + 10))
    dibujo_texto_principal = ImageDraw.Draw(img_text_secundario)
    y_text = 0

    alto_img = 0
    lines = textwrap.wrap(texto_secundario, width = 85) # <--- Probar a modificar esto
    for line in lines:
        line_width, line_height = fuente_secundaria.getsize(line)
        dibujo_texto_principal.text(((ancho_imagen_marco - line_width) / 2, y_text), line, font=fuente_secundaria, fill = 'white')
        alto_img += line_height
        y_text += line_height

    img_text_secundario.save(f'img_texts/secundario/{num_img}.png')
    return alto_img


def crear_imagen_final(alto_img_principal, alto_img_secundario, alto_img_marco, video, coordenada_img_baner_x, coordenada_img_baner_y, marco):
    num_img = str(leer_num_img()) # <--- Llamo a la funcion para leer el numero de imagen

    video_principal = video
    # duracion = video_principal.duration
    # img_baner = Image.open('recursos/baner.png')
    img_texto_principal = Image.open(f'img_texts/principal/{num_img}.png')
    img_texto_secundario = Image.open(f'img_texts/secundario/{num_img}.png')

    alto_img = alto_img_principal + alto_img_secundario + alto_img_marco

    imagen_final = Image.new('RGB', (650, alto_img + 20 + 15)) # <--- El 10 es una compensacion para que el texto no quede tan pegado por abajo

    imagen_final.paste(marco, (0, 0))
    # imagen_final.paste(video_principal, (33, 33))
    # imagen_final.paste(img_baner, (int(coordenada_img_baner_x), int(coordenada_img_baner_y)))
    imagen_final.paste(img_texto_principal, (0, alto_img_marco))
    imagen_final.paste(img_texto_secundario, (0, alto_img_marco + alto_img_principal + 15))

    imagen_final.save(f'exported/{num_img}.png')

    clipMarco = ImageClip(f'exported/{num_img}.png')
    clipMarco = clipMarco.set_duration(video_principal.duration)

    clipBaner = ImageClip(f'recursos/baner.png')
    clipBaner = clipBaner.set_duration(video_principal.duration)

    videoFinal = CompositeVideoClip([clipMarco, video_principal.set_position((33, 33)), clipBaner.set_position((int(coordenada_img_baner_x), int(coordenada_img_baner_y)))])
    videoFinal.write_videofile(f'exported/{num_img}.mp4', fps = video_principal.fps)
