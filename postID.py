path = 'recursos/post_id.txt'

def leer_postID():
    with open(path, 'r', encoding="utf8") as archivo:
        postID = int(archivo.readline())
        
    return postID


def reestablecer_postID(post_id):
    with open(path, 'w', encoding="utf8") as archivo:
        archivo.write(post_id)