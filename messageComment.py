from imgNumber import leer_num_img


def mensaje_comentario():
    num = leer_num_img()

    if (num % 10 == 0):
        return 'Ya hay una publicación más reciente.'
    elif (num % 10 == 1):
        return 'Ya hay una publicación más reciente. Ya no se tomarán en cuenta estas peticiones.'
    elif (num % 10 == 2):
        return 'Ya no se tomarán en cuenta estas peticiones.'
    elif (num % 10 == 3):
        return 'Ya existe una publicación más reciente.'
    elif (num % 10 == 4):
        return 'Estos comentarios ya no serán tomados en cuenta.'
    elif (num % 10 == 5):
        return 'Ya hay una publicación más reciente.'
    elif (num % 10 == 6):
        return 'Ya hay una publicación más reciente. Ya no se tomarán en cuenta estas peticiones.'
    elif (num % 10 == 7):
        return 'Ya no se tomarán en cuenta estas peticiones.'
    elif (num % 10 == 8):
        return 'Ya existe una publicación más reciente.'
    elif (num % 10 == 9):
        return 'Estos comentarios ya no serán tomados en cuenta.'
