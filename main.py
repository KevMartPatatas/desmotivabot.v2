import time
import schedule
import facebook as fb
from getComments import getComments
from crearImagen import crear_marco
from crearVideo import crear_marco_video
from imgNumber import *
from postID import *
from decouple import config
import os
from datetime import datetime
import requests
from messageComment import mensaje_comentario
link_guia = 'https://www.facebook.com/permalink.php?story_fbid=pfbid0t6vpdYhxxMTqYVEJwbija87vDduCcs9TUAheHQL6rKsMSKMrdZeA6JSibcs47z7ql&id=100088637787864'

#<--- autenticación de la API facebook --->
os.environ['TOKEN'] = config('TOKEN')
token_de_acceso = os.environ['TOKEN']
graph = fb.GraphAPI(access_token = token_de_acceso)

def main():
    num_img = leer_num_img()
    
    datos_retornados = getComments()
    if len(datos_retornados) > 1:
        texto_principal, texto_secundario, num_voto_mayor, num_total_req, tipo_archivo, src = datos_retornados

        if tipo_archivo == 'photo':
            crear_marco(texto_principal, texto_secundario)
            extension = 'png'
        elif tipo_archivo == 'video_inline':
            crear_marco_video(texto_principal, texto_secundario)
            extension = 'video'

        repetir = True
        while repetir == True:
            try:
                post_id_viejo = leer_postID()
                hora, minuto, segundo = obtenerHora()
                horaActual = f'{str(hora)}:{str(minuto)}:{str(segundo)}'
                mensaje = f'Su petición.\nNúmero de imagen: {str(num_img)}\nHora: {horaActual}'
                # mensaje = 'EL BOT ESTÁ DE VUELTA!'

                if extension == 'png':
                    publicar_imagen = graph.put_photo(image = open(f'exported/{str(num_img)}.png', 'rb'), message = mensaje)
                    post_id_nuevo = publicar_imagen['id']
                    print(publicar_imagen['id'])

                    repetir = True
                    while repetir == True:
                        try:
                            graph.put_comment(object_id = post_id_viejo, message = mensaje_comentario())
                            repetir = False
                        except Exception as e:
                            print(e)
                            repetir = True
                            time.sleep(1)
                else:
                    if extension == 'video':
                        url_solicitar_subir_video = 'https://graph.facebook.com/111924031719727/videos'
                        fp = f'exported/{str(num_img)}.mp4'
                        files = {'source': open(fp, 'rb')}
                        payload = {'access_token': token_de_acceso, 'title': f'Petición No. {str(num_img)}', 'description': mensaje}

                        try:
                            requests.post(url_solicitar_subir_video, files = files, data = payload, verify = False)
                            time.sleep(15)
                            url_solicitar_subir_video = 'https://graph.facebook.com/111924031719727/videos?access_token=' + token_de_acceso
                            videos_subidos = requests.get(url_solicitar_subir_video).json()
                            post_id_nuevo = videos_subidos['data'][0]['id']
                            print(videos_subidos['data'][0]['id'])

                            repetir = True
                            while repetir == True:
                                try:
                                    graph.put_comment(object_id = post_id_viejo, message = mensaje_comentario())
                                    repetir = False
                                except Exception as e:
                                    print(e)
                                    repetir = True
                                    time.sleep(1)
                        except:
                            pass
                post_id_nuevo = post_id_nuevo # <--- Si esto me da probemas despues, le agrego el ID de la pagina.
                repetir = False
            except:
                print('No se puede poner el comentario')
                time.sleep(5)
                repetir = True

        repetir = True
        while repetir == True:
            try:
                graph.put_comment(object_id = post_id_nuevo, message = f'Número de votos: {str(num_voto_mayor)}\nNúmero de peticiones en la publicación anterior: {str(num_total_req)}\nPor favor, vota negativamente las malas imágenes y vota positivamente las buenas imágenes.\n\n¿Como hacer un petición? Comenta:\n!req\nLínea de texto párrafo 2\nLínea de texto párrafo 3\ny añade una imagen\n{link_guia}\n\nSistema de votación:\n\U0001F44D, \U00002764, Me importa, \U0001F606, \U0001F632: +1 voto \U0001F446.\n\U0001F625, \U0001F621: -1 voto \U0001F447.\n\nID del post: {post_id_nuevo}.')
                print('Comentario agregado')
                repetir = False
            except:
                print('No se puede poner el comentario. ID invalido')
                time.sleep(5)
                repetir = True

        reestablecer_postID(post_id_nuevo)
        reescribir_numero_img()
    else:
        print('Ningun comentario valido')
        hora, minuto, segundo = obtenerHora()
        print(f'{str(hora)}:{str(minuto)}:{str(segundo)}\n')
        

def obtenerHora():
    now = datetime.now()
    hora = now.hour - 6 # <--- El 6 es por el utf-6
    minuto = now.minute
    segundo = now.second

    if hora < 0:
        hora = 24 + hora
    
    if hora < 10:
        hora = f'0{str(hora)}'
    if minuto < 10:
        minuto = f'0{str(minuto)}'
    if segundo < 10:
        segundo = f'0{str(segundo)}'

    return [hora, minuto, segundo]

if __name__ == '__main__':
    # main()
    schedule.every().hour.at(':00').do(main)
    # schedule.every().hour.at(':05').do(main)
    # schedule.every().hour.at(':10').do(main)
    schedule.every().hour.at(':15').do(main)
    # schedule.every().hour.at(':20').do(main)
    # schedule.every().hour.at(':25').do(main)
    schedule.every().hour.at(':30').do(main)
    # schedule.every().hour.at(':35').do(main)
    # schedule.every().hour.at(':40').do(main)
    schedule.every().hour.at(':45').do(main)
    # schedule.every().hour.at(':50').do(main)
    # schedule.every().hour.at(':55').do(main)

    while True:
        hora, minutos, segundo = obtenerHora()

        if int(hora) == 3:
            if int(minutos) <= 1:
                schedule.run_pending()

        elif int(hora) <= 2 or int(hora) >= 7:
            schedule.run_pending()

        time.sleep(10)
        