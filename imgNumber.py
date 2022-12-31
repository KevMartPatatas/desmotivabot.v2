path = 'recursos/img_number.txt'

def leer_num_img():
    with open(path, 'r', encoding="utf8") as archivo:
        numero_img = int(archivo.readline())
        
    return numero_img



def reescribir_numero_img():
    numero_imagen = leer_num_img()

    with open(path, 'w', encoding="utf8") as archivo:
        archivo.write(str(numero_imagen + 1))
