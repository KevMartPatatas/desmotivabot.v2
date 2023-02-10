import facebook as fb
import requests
import time
from getReactions import get_reactions
from descargarArchivos import *
from postID import leer_postID
from decouple import config
import os

os.environ['TOKEN'] = config('TOKEN')
token_de_acceso = os.environ['TOKEN']
graph = fb.GraphAPI(access_token = token_de_acceso)
link_guia = 'https://www.facebook.com/permalink.php?story_fbid=pfbid02E7ubrXm58EGj6Dyz8jxxhMCotx9MW6JcyX6JDYhgp6jaGqSS1FZUkNaHd9vhDRaNl&id=100087511416286'

def getComments():
    num_voto_mayor = -100 # <--- Inicializo la variable con esa valor ya que es muy bajo
    num_total_req = 0 # <--- Esto me sirve para obtener el numero total de los pedidos en la publicacion anterior
    id_post = leer_postID() # <--- Guardo en una variable el ID del post

    comentarios = graph.get_connections(id = f'111924031719727_{id_post}', connection_name = 'comments') # <--- Solicito todos los comentarios del post

    for comentario in comentarios['data']: # <--- Itero los comenterios
        id_comentario = comentario['id'] # <--- Me da el ID del comentario

        url_solicitar_informacion_comentario = "https://graph.facebook.com/" + id_comentario + "?fields=attachment&access_token=" + token_de_acceso # <--- Preparo el link para mandar una peticion HTTP a la api, para conseguir informacion de los coementarios

        repetir = True
        while repetir == True:
            try:
                solicitud_informacion_comentario = requests.get(url_solicitar_informacion_comentario).json() # <--- Hago la solicitud y guardo la informacion en esa variable
                repetir = False
            except:
                print('se repite')
                time.sleep(5)
                repetir = True

        if (len(solicitud_informacion_comentario) == 2): # <--- Me comprueba que el comentario tenga una archivo adjunto
            tipo_archivo_adjunto = solicitud_informacion_comentario['attachment']['type'] # <--- Me devulve el tipo de archivo adjunto

            if (tipo_archivo_adjunto == 'photo' or tipo_archivo_adjunto == 'video_inline'): # <--- Me comprueba que el archivo adjunto sea una foto o una foto
                mensaje = comentario['message'] # <--- Guardo el mensaje del comentario
                separar_texto_mensaje = mensaje.split('\n') # <--- Separa el mensaje del comentario por cada salto de linea y me da un array de eso

                while '' in separar_texto_mensaje: # <--- Esto me sirve para que pueda haber tantos espacios de parrafo como sea posible, ya que me elimina esos espacios en blanco en el array del mensaje
                    separar_texto_mensaje.remove('')

                if (len(separar_texto_mensaje) == 3 or len(separar_texto_mensaje) == 2): # <--- Me comprueba que, en el array existan tres elementos
                    comando = separar_texto_mensaje[0].lower()

                    if (comando.strip() == '!req'): # <--- Me comprueba que el primer elemento del array sea !req
                        # Si en algun futuro esto me da problema con el limite de solicitudes de la API, tratare de hacer esto pero con cada solicitud individual
                        repetir = True
                        while repetir == True:
                            try:
                                voto_total = get_reactions(id_comentario) # <--- Llamo a la funcion para conseguir el numero de votos, pasandole como parametro el id del comentario
                                repetir = False
                            except:
                                time.sleep(5)
                                repetir = True

                        num_total_req += 1

                        if (voto_total >= num_voto_mayor): # <--- Comprueba que, el numero de votos sea mayor al numero mayor de votos en cada iteracion
                            num_voto_mayor = voto_total # <--- guardo el voto total en la variable de numero de votos mayor en cada iteracion
                            
                            id_comentario_final = id_comentario # <--- Me da el id final del comentario con el numero mayor de votos
                            mensaje_final = mensaje # <--- Me da el mensaje final del comentario con el numero mayor de votos
                            texto_principal = separar_texto_mensaje[1] # <--- Me da el texto principal (segunda linea) final del comentario con el numero mayor de votos


                            if len(separar_texto_mensaje) == 3:
                                texto_secundario = separar_texto_mensaje[2] # <--- Me da el texto secundario (tercera linea) final del comentario con el numero mayor de votos
                            else:
                                texto_secundario = ''
                            tipo_archivo = tipo_archivo_adjunto

                            if tipo_archivo_adjunto == 'photo':
                                src = solicitud_informacion_comentario['attachment']['media']['image']['src'] # <--- Me da la url de la imaagen para descargar
                            elif tipo_archivo_adjunto == 'video_inline':
                                src = solicitud_informacion_comentario['attachment']['media']['source']

                else:
                    try:
                        comando = separar_texto_mensaje[0].lower()
                        if comando.strip() in separar_texto_mensaje:
                            graph.put_comment(object_id = id_comentario, message = f'Su petición es invalida, lee esto para saber cómo hacer una petición: {link_guia}')

                    except:
                        pass

    if num_voto_mayor != -100: # <--- Despues de salir del bucle. Simplemente me comrpueba que, de todos los comentarios haya por lo menos un comentario que cumpla con las caracteristicas
        if tipo_archivo == 'photo':
            descargar_imagen(src) # <--- Llamo a la funcion para descargar la imagen, le paso como parametro el link directo de la imagen
        else:
            if tipo_archivo == 'video_inline':
                descargar_video(src)
        return [texto_principal, texto_secundario, num_voto_mayor, num_total_req, tipo_archivo, src]

    else:
        return [num_voto_mayor]
