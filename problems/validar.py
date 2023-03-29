def validar(s):
    # Convertimos el string a minúsculas
    s = s.lower()
    # Inicializamos un diccionario para contar las letras
    contadores = {'h': 0, 'o': 0, 'l': 0, 'a': 0}
    # Iteramos por cada letra del string
    for letra in s:
        # Si la letra no es una de las letras de "hola", no es válido
        if letra not in contadores:
            return "FALSO"
        # Si es una letra válida, aumentamos el contador correspondiente
        contadores[letra] += 1
    # Comprobamos que se haya escrito cada letra al menos una vez
    for letra, contador in contadores.items():
        if contador == 0:
            return "FALSO"
    # Comprobamos que se hayan escrito las letras en el orden correcto
    if s.find('h') < s.find('o') < s.find('l') < s.rfind('l') < s.find('a'):
        return "VERDADERO"
    else:
        return "FALSO"

if __name__ == '__main__': 
    print((validar("hola")))
    print((validar("hhhhooooollllllaaaaaa")))
    print((validar('hhhlllllloooollllla')))
