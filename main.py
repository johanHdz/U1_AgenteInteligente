import pygame
import random
import astar
import time
from tkinter import messagebox


class Maze:
    def __init__(self):
        #         X   0  1  2  3  4  5  6  7  8  9     Y
        self.mapa = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # 0
                     [0, 1, 0, 0, 0, 1, 0, 1, 0, 1],  # 1
                     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # 2
                     [0, 0, 0, 1, 0, 0, 0, 1, 1, 0],  # 3
                     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # 4
                     [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],  # 5
                     [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # 6
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # 7
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 1],  # 8
                     [1, 1, 0, 0, 0, 0, 0, 1, 0, 0]]  # 9

        self.mapaR = [[self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()],
                      [self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r(), self.r()]]

        self.muros = []
        self.camino = []
        self.personaje = None
        self.meta = None
        self.objetivos = []
        self.posXPsj = None
        self.posYPsj = None
        self.posXMeta = None
        self.posYMeta = None

    def r(self):
        return random.randint(0, 1)

    def construir_mapa(self):
        x, y, px, py = 0, 0, 0, 0

        for fila in self.mapaR:
            for celda in fila:
                if celda == 1:
                    self.muros.append(pygame.Rect(x, y, 60, 60))
                elif celda == 0:
                    self.camino.append([x, y, py, px])
                x = x + 60
                px += 1
            x, px = 0, 0
            py += 1
            y = y + 60

    def dibujar_mapa(self, ventana):
        x, y = 0, 0
        imgMuro = pygame.image.load("src/agua.jpg").convert()
        imgSuelo = pygame.image.load("src/cesped.jpeg").convert()

        for fila in self.mapaR:
            for celda in fila:
                if celda == 1:
                    ventana.blit(imgMuro, (x, y))
                else:
                    ventana.blit(imgSuelo, (x, y))
                x = x + 60
            x = 0
            y = y + 60

    def dibujar_personaje(self, ventana):
        imgPsj = pygame.image.load("src/personaje.png").convert()
        imgPsj.set_colorkey((0, 255, 0))
        ventana.blit(imgPsj, (self.personaje.x, self.personaje.y))

    def dibujar_objetivo(self, ventana):
        imgObjetivo = pygame.image.load("src/objetivo.png").convert()
        imgObjetivo.set_colorkey((255, 0, 0))
        ventana.blit(imgObjetivo, (self.meta.x, self.meta.y))

    def dibujar_camino(self, ventana, est):
        imgSuelo = pygame.image.load("src/muro_2.jpeg").convert()
        a = list(est)
        x = (a[0]) * 60
        y = (a[1]) * 60
        self.x = x
        self.y = y
        ventana.blit(imgSuelo, (self.y, self.x))

    def reiniciar_juego(self):
        randPsj = random.randint(0, (len(self.camino) - 1))
        randObj = random.randint(0, (len(self.camino) - 1))
        self.personaje = pygame.Rect(self.camino[randPsj][0], self.camino[randPsj][1], 60, 60)
        self.posXPsj = self.camino[randPsj][3]
        self.posYPsj = self.camino[randPsj][2]
        while len(self.objetivos) != 0:
            self.objetivos.pop()
        while True:
            if randPsj == randObj:
                randObj = random.randint(0, (len(self.camino) - 1))
            else:
                self.meta = pygame.Rect(self.camino[randObj][0], self.camino[randObj][1], 60, 60)
                self.posXMeta = self.camino[randObj][3]
                self.posYMeta = self.camino[randObj][2]
                self.objetivos.append(self.meta)
                break
        print("Posición del Personaje: ("+str(maze.posYPsj)+", "+str(maze.posXPsj)+")")
        print("Posición del Objetivo: ("+str(maze.posYMeta)+", "+str(maze.posXMeta)+")")


# Inicializar pygame
pygame.init()

# Variables
Ancho, Largo = 800, 600
reloj = pygame.time.Clock()

# Fuente
fuenteLetra = pygame.font.SysFont("console", 18)
NEGRO = (0, 0, 0)
a = []
b = []

# Ventana
ventana = pygame.display.set_mode((Ancho, Largo))

# Iniciación de la clase y construcción del mapa
maze = Maze()
maze.construir_mapa()
maze.reiniciar_juego()
jugando = True
personajeVelocidadX, personajeVelocidadY = 0, 0

# Bucle principal donde se ejecutara el juego
while jugando:
    reloj.tick(15)
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

        # Detección de teclas
        if event.type == pygame.KEYDOWN:
            # Finalizar juego
            if event.key == pygame.K_ESCAPE:
                jugando = False
            # Reiniciar juego
            if event.key == pygame.K_r:
                maze.reiniciar_juego()

            # Iniciar agente inteligente
            if event.key == pygame.K_RETURN:
                camino, listaMovimientos, informacion = astar.astar(maze.mapaR, (maze.posYPsj, maze.posXPsj), (maze.posYMeta, maze.posXMeta))
                if camino == 1 or listaMovimientos == 1 or informacion == 1:
                    # Error
                    messagebox.showinfo("No solución", "No se encontró solución")
                else:
                    # Imprimimos el camino y los movimientos que realizó el agente
                    print("Camino:", camino)
                    print("Movimientos que realizó:", listaMovimientos)
                    # Texto del Camino
                    a = listaMovimientos
                    b = camino
                    # Creación de un archivo de texto donde se guarda información de los nodos
                    for fila in informacion:
                        print(fila)
                    with open("Información.txt", "w") as archivo:
                        for fila in informacion:
                            archivo.write(str(fila) + "\n")
                    # Lógica de Movimiento
                    for recorrido in listaMovimientos:
                        # Movimiento hacía arriba
                        if recorrido == "arriba":
                            personajeVelocidadX = 0
                            personajeVelocidadY = -60
                        # Movimiento hacía abajo
                        elif recorrido == "abajo":
                            personajeVelocidadX = 0
                            personajeVelocidadY = 60
                        # Movimiento hacía la izquierda
                        elif recorrido == "izquierda":
                            personajeVelocidadX = -60
                            personajeVelocidadY = 0
                        # Movimiento hacía la derecha
                        elif recorrido == "derecha":
                            personajeVelocidadX = 60
                            personajeVelocidadY = 0
                        # Actualizamos la posición del personaje
                        maze.personaje.x = maze.personaje.x + personajeVelocidadX
                        maze.personaje.y = maze.personaje.y + personajeVelocidadY
                        # Colisión con el objetivo
                        for premio in maze.objetivos:
                            if maze.personaje.collidepoint(premio.centerx, premio.centery):
                                maze.objetivos.remove(premio)
                        # Dibujamos nuevamente los elementos gráficos
                        maze.dibujar_mapa(ventana)
                        maze.dibujar_personaje(ventana)
                        if len(maze.objetivos) != 0:
                            maze.dibujar_objetivo(ventana)
                        # Actualizamos la pantalla
                        pygame.display.flip()
                        pygame.display.update()
                        # Hacemos que el juego "se detenga" por 0.5 segundos
                        time.sleep(0.5)

    # Graficación de los elementos del Mapa
    ventana.fill((255, 255, 255))
    # Graficación del mapa
    maze.dibujar_mapa(ventana)
    # Graficación del Personaje
    maze.dibujar_personaje(ventana)
    # Textos
    texto = fuenteLetra.render("LISTA MOVIMIENTOS:", True, NEGRO)
    y = 40
    for i in a:
        mensaje = fuenteLetra.render(i, True, NEGRO)
        ventana.blit(mensaje, (650, y))
        y = y + 30
    ventana.blit(texto, (600, 0))
    # Dibujar Camino
    c = len(b) - 1
    for i in range(c):
        maze.dibujar_camino(ventana, b[i])
    # Graficación del Objetivo
    if len(maze.objetivos) != 0:
        maze.dibujar_objetivo(ventana)
    # Actualización de la pantalla
    pygame.display.flip()
    pygame.display.update()
