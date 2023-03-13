from tkinter import messagebox


class Nodo():
    """Una clase de Nodo para el algoritmo A*"""

    def __init__(self, padre=None, posicion=None, movimiento=None):
        self.padre = padre
        self.posicion = posicion
        self.movimiento = movimiento

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otra):
        return self.posicion == otra.posicion


def astar(maze, inicio, final):
    """Devuelve un camino en forma de lista desde el inicio hasta el final en en laberinto dado"""

    # Crear nodo inicial y final
    nodo_inicial = Nodo(None, inicio)
    nodo_inicial.g = nodo_inicial.h = nodo_inicial.f = 0
    nodo_final = Nodo(None, final)
    nodo_final.g = nodo_final.h = nodo_final.f = 0

    # Inicializar tanto la lista abierta como la cerrada
    lista_abierta = []
    lista_cerrada = []

    # Añade el nodo inicial
    lista_abierta.append(nodo_inicial)
    # Bandera para cuando no pueda encontrar un camino
    band = 0
    # Bucle hasta encontrar el final
    while len(lista_abierta) > 0:

        # Obtener el nodo actual
        nodo_actual = lista_abierta[0]
        indice_actual = 0
        for indice, elemento in enumerate(lista_abierta):
            if elemento.f < nodo_actual.f:
                nodo_actual = elemento
                indice_actual = indice

        # Elimina el nodo actual de la lista abierta, añade node actual a la lista cerrada
        lista_abierta.pop(indice_actual)
        lista_cerrada.append(nodo_actual)
        band += 1

        # Si se encontró el objetivo
        if nodo_actual == nodo_final:
            ruta = []
            listaMovimientos = []
            informacion = []
            actual = nodo_actual
            while actual is not None:
                informacion.append("Nodo en la posición " + str(actual.posicion) + "\n"
                                   "f: " + str(actual.f) + "\n" +
                                   "g: " + str(actual.g) + "\n" +
                                   "h: " + str(actual.h))
                ruta.append(actual.posicion)
                listaMovimientos.append(actual.movimiento)
                actual = actual.padre
            listaMovimientos.pop()
            # Regresa el camino, los movimientos e informacion en forma inversa
            return ruta[::-1], listaMovimientos[::-1], informacion[::-1]

        # Generar hijos
        hijos = []  # Y   X
        # Bandera para cuando no pueda encontrar un camino
        flag = 0
        # Movimiento          izq       der    arriba   abajo
        for nueva_posicion in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            mov = ""
            # Obtener la posición del nodo
            posicion_nodo = (nodo_actual.posicion[0] + nueva_posicion[0], nodo_actual.posicion[1] + nueva_posicion[1])

            # Asegurar de que está dentro del rango
            if posicion_nodo[0] > (len(maze) - 1) or posicion_nodo[0] < 0 or posicion_nodo[1] > (
                    len(maze[len(maze) - 1]) - 1) or posicion_nodo[1] < 0:
                flag += 1
                continue

            # Asegurar que sea un camino y no un muro
            if maze[posicion_nodo[0]][posicion_nodo[1]] != 0:
                flag += 1
                continue

            # Conocer movimiento realizó
            if nueva_posicion == (0, -1):
                mov = "izquierda"
            elif nueva_posicion == (0, 1):
                mov = "derecha"
            elif nueva_posicion == (-1, 0):
                mov = "arriba"
            elif nueva_posicion == (1, 0):
                mov = "abajo"

            # Crea un nuevo nodo
            nuevo_nodo = Nodo(nodo_actual, posicion_nodo, mov)

            # Se añade a la lista de hijos
            hijos.append(nuevo_nodo)

        # Bucle para recorrer la lista de hijos
        if band < 100 and flag != 4:
            for hijo in hijos:

                # Un hijo se encuentra en la lista cerrada
                for hijo_en_lista_cerrada in lista_cerrada:
                    if hijo == hijo_en_lista_cerrada:
                        continue

                # Crea los valores f, g, y h
                hijo.g = nodo_actual.g + 1
                hijo.h = ((hijo.posicion[0] - nodo_final.posicion[0]) ** 2) + (
                            (hijo.posicion[1] - nodo_final.posicion[1]) ** 2)
                hijo.f = hijo.g + hijo.h

                # Hijo ya se encuentra en la lista abierta
                for nodo_abierto in lista_abierta:
                    if hijo == nodo_abierto and hijo.g > nodo_abierto.g:
                        continue

                # Añade el Hijo a la lista abierta
                lista_abierta.append(hijo)
        else:
            return 1, 1, 1

"""
#     X   0  1  2  3  4  5  6  7  8  9     Y
mapa2 = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 0
         [1, 1, 1, 0, 0, 1, 0, 1, 0, 1],  # 1
         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # 2
         [0, 0, 0, 1, 0, 0, 0, 1, 1, 0],  # 3
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 4
         [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],  # 5
         [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # 6
         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # 7
         [0, 0, 0, 1, 1, 1, 0, 0, 0, 1],  # 8
         [1, 1, 0, 0, 0, 0, 0, 1, 0, 0]]  # 9

camino, movimientos, informacion = astar(mapa2, (0, 0), (0, 4))
if camino == 1 or movimientos == 1:
    messagebox.showinfo("No solución", "No se encontró solución")
else:
    print("Camino:", camino)
    print("Movimientos que realizó:", movimientos)
    with open("Información.txt", "w") as archivo:
        for fila in informacion:
            archivo.write(str(fila)+"\n") """
