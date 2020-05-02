from colorama import init, Fore, Back

init()


# Esta es la función que crea la matriz utilizada en CYK
def crearTabla(palabra):
    print(Fore.MAGENTA + "Se crea la tabla vacia con '0'")
    tabla = [[['Ø']] * (len(palabra) - i) for i in range(len(palabra))]
    return tabla


# La función busca y devuelve si la palabra está entre los resultados de los no terminales
def encontrarGramatica(grammar, simbolo):
    print(Fore.GREEN + "Simbolo: " + simbolo)
    generadores = []
    for key in grammar.keys():
        print(Fore.GREEN, end="")
        print(grammar[key])
        if simbolo in grammar[key]:
            print("El simbolo coincidio con uno generador, con este: ", end="")
            print(key)
            generadores.append(key)
    if not generadores:
        print("0")
        return "Ø"
    else:
        print(generadores)
        return generadores


# Aquí se hace el producto cartesiano después de lo cual la función anterior se aplica en cada resultado
def producto(gramatica, lista1, lista2):
    lista = []
    for i in lista1:
        print(Fore.RED, end="")
        print(i)
        for j in lista2:
            print(j)
            wordsFound = encontrarGramatica(gramatica, i + j)
            print(Fore.RED, end="")
            print(wordsFound)
            if wordsFound != "Ø":
                for word in wordsFound:
                    lista.append(word)
    print(Fore.RED, end="")
    print(lista)
    if not lista:
        return ['Ø']
    else:
        return lista


# Esta función elimina los duplicados de las reuniones y O's cuando proceda
def repetidos(union):
    # para no tener repetidos ponemos un set
    union = set(union)
    # recorremos la lista pa ver si hay un 0 y borrarlo
    if 'O' in union and len(union) > 1:
        union.remove('Ø')
    union = list(union)
    return union


# Aquí se encuentra y muestra la derivación de la palabra
def derive(grammar, palabra, inicio):
    #print(Fore.MAGENTA + inicio)
    if inicio.islower():
        if inicio == palabra:
            return inicio
    else:
        #print(Fore.MAGENTA + str(len(inicio)))
        if len(inicio) <= len(palabra):
            for i in range(len(inicio)):
                if inicio[i] in grammar.keys():
                    #print(grammar[inicio[i]])
                    for terminal in grammar[inicio[i]]:
                        #print(terminal)
                        #print("---" + inicio[:i] + terminal + inicio[(i + 1):])
                        ret = derive(grammar, palabra, inicio[:i] + terminal + inicio[(i + 1):])
                        if ret is not None:
                            return inicio + " -> " + ret


# Este es el algoritmo CYK
def CYK(gramatica, palabras):
    for palabra in palabras:
        print(Fore.YELLOW + "------------------------------crearTabla-------------------------------------")
        print(Fore.MAGENTA + "La palabra es: " + palabra)
        tabla = crearTabla(palabra)
        print(tabla)
        n = len(palabra)
        print("Tamaño de la palabra: " + str(n))
        for j in range(n):
            print(Fore.YELLOW + "------------------------------findInGrammar-------------------------------------")
            tabla[0][j] = encontrarGramatica(gramatica, palabra[j])
            print(Fore.LIGHTRED_EX + "valor en la posicion 0 "+str(j)+" ", end="")
            print(tabla[0][j])
            print(tabla)
        for i in range(1, n):
            print(Fore.BLUE + "i = "+str(i))
            for j in range(0, n - i):
                print(Fore.BLUE + "j = " + str(j))
                union = []
                for k in range(0, i):
                    print(Fore.BLUE + "k = " + str(k))
                    print(Fore.BLUE, end="")
                    print(tabla[k][j])
                    print(tabla[i - 1 - k][j + 1 + k])
                    print(Fore.YELLOW + "------------------------------product-------------------------------------")
                    union += producto(gramatica, tabla[k][j], tabla[i - 1 - k][j + 1 + k])
                    print(Fore.BLUE, end="")
                    print(union)
                print(Fore.YELLOW + "------------------------------normalize-------------------------------------")
                tabla[i][j] = repetidos(union)
                print(Fore.RED, end="")
                print(tabla[i][j])
                print(tabla)
        # for row in table:
        #      print(' '.join([str(elem) for elem in row]))
        if 'S' not in tabla[n - 1][0]:
            print(Fore.RED + "-La palabra: " + palabra + " no pertenece a la gramatica")
        else:
            print(Fore.GREEN + "-La palabra: " + palabra + " pertenece a la gramatica, y una derivacion es: " +
                  derive(gramatica, palabra, "S"))


gramatica = {}
palabras = []
f = open("Data.txt", "r")
for x in f.readlines():
    x = x.strip()
    print("x: " + x)
    if '->' in x:
        split = x.split(' -> ')
        print("Split: ", end="")
        print(split)
        print("Simbolo Generador: " + split[0])
        if split[0] in gramatica:
            print("-Si estaba en la lista de gramatica")
            print("---Simbolo Generador: " + split[0])
            print("Gramatica: ", end="")
            print(gramatica)
            gramatica[split[0]].append(split[1])
            print("Gramatica despues: ", end="")
            print(gramatica)
            print("---------------------------------------")
        else:
            print("-No estaba en la lista de gramatica")
            print("Simbolo Generador: " + split[0])
            print("Simbolos Generados: " + split[1])
            gramatica[split[0]] = [split[1]]
            print("Gramatica: ", end="")
            print(gramatica)
            print("---------------------------------------")
    else:
        print("Agregando la palabra " + x)

        palabras.append(x)
        print(palabras)
f.close()
print("---------------------------------------")
# Gramatica es un diccionario
print("Gramatica: ", end="")
print(gramatica)
print("Palabras: ", end="")
print(palabras)
print("---------------------------------------")

print(Fore.YELLOW + "------------------------------CYK--------------------------------------------------------------")
CYK(gramatica, palabras)
