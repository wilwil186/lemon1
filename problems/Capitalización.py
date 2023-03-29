def capitalizar(s):
    # Dividimos el string en palabras
    palabras = s.split()
    # Iteramos por cada palabra
    for i in range(len(palabras)):
        # Obtenemos la primera letra y la convertimos a mayúscula
        primera_letra = palabras[i][0].upper()
        # Concatenamos la primera letra con el resto de la palabra
        palabras[i] = primera_letra + palabras[i][1:]
    # Unimos las palabras capitalizadas en un solo string
    return " ".join(palabras)

if __name__ == "__main__":
    print(capitalizar('DatoS'))
    print((capitalizar('lumon')))
    print((capitalizar('anAliTicA')))