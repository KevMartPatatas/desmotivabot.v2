import requests
import os
from decouple import config

os.environ['TOKEN'] = config('TOKEN')
token_de_acceso = os.environ['TOKEN']

def get_reactions(id_comentario):
    url_solicitar_like = 'https://graph.facebook.com/' + id_comentario + '?fields=reactions.type(LIKE).limit(0).summary(total_count)&access_token=' + token_de_acceso
    solicitar_like = requests.get(url_solicitar_like).json()

    url_solicitar_love = 'https://graph.facebook.com/' + id_comentario + '?fields=reactions.type(LOVE).limit(0).summary(total_count)&access_token=' + token_de_acceso
    solicitar_love = requests.get(url_solicitar_love).json()

    url_solicitar_wow = 'https://graph.facebook.com/' + id_comentario + '?fields=reactions.type(WOW).limit(0).summary(total_count)&access_token=' + token_de_acceso
    solicitar_wow = requests.get(url_solicitar_wow).json()

    url_solicitar_haha = 'https://graph.facebook.com/' + id_comentario + '?fields=reactions.type(HAHA).limit(0).summary(total_count)&access_token=' + token_de_acceso
    solicitar_haha = requests.get(url_solicitar_haha).json()

    url_solicitar_sad = 'https://graph.facebook.com/' + id_comentario + '?fields=reactions.type(SAD).limit(0).summary(total_count)&access_token=' + token_de_acceso
    solicitar_sad = requests.get(url_solicitar_sad).json()

    url_solicitar_angry = 'https://graph.facebook.com/' + id_comentario + '?fields=reactions.type(ANGRY).limit(0).summary(total_count)&access_token=' + token_de_acceso
    solicitar_angry = requests.get(url_solicitar_angry).json()

    numero_likes = solicitar_like['reactions']['summary']['total_count']
    numero_love = solicitar_love['reactions']['summary']['total_count']
    numero_wow = solicitar_wow['reactions']['summary']['total_count']
    numero_haha = solicitar_haha['reactions']['summary']['total_count']
    numero_sad = solicitar_sad['reactions']['summary']['total_count']
    numero_angry = solicitar_angry['reactions']['summary']['total_count']

    voto_total = numero_likes + numero_love + numero_wow + numero_haha - numero_sad - numero_angry

    return voto_total
