import pygame
from pygame.locals import *
import random

pygame.init()

pygame.display.set_caption ("BRAYAN BAD")

ancho = 800
alto = 600
cantidadPolicias = 10

pantalla = pygame.display.set_mode( (ancho, alto) )
pygame.key.set_repeat(1,25)
reloj = pygame.time.Clock()

imagenLadron = pygame.image.load("ladron.png")
rectanguloLadron = imagenLadron.get_rect()
imagenPatrullero = pygame.image.load("patrullero.png")
rectanguloPatrullero = imagenPatrullero.get_rect()
imagenPolicia = pygame.image.load("policia.png")
rectangulosPolicias = { }
PoliciasVisibles = { }
velocidadesX = { }
velocidadesY = { }
imagenDisparo = pygame.image.load("disparo.png")
rectanguloDisparo = imagenDisparo.get_rect()

imagenPresent = pygame.image.load("juegoIntro.png")
rectanguloPresent = imagenPresent.get_rect()
rectanguloPresent.top = 60
rectanguloPresent.left = 80

imagenMenu = pygame.image.load("menu.png")
rectanguloMenu = imagenMenu.get_rect()
rectanguloMenu.top = 60
rectanguloMenu.left = 80

imagenCreditos = pygame.image.load("creditos.png")
rectanguloCreditos = imagenCreditos.get_rect()
rectanguloCreditos.top = 60
rectanguloCreditos.left = 80

letra30 = pygame.font.SysFont("Arial", 30)

imagenTextoPresent = letra30.render('Pulsa Espacio para ir al menu',
    True, (200,200,200), (0,0,0) )
rectanguloTextoPresent = imagenTextoPresent.get_rect()
rectanguloTextoPresent.centerx = pantalla.get_rect().centerx
rectanguloTextoPresent.centery = 520

letra18 = pygame.font.SysFont("Arial", 18)

pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play(-1)


def completo ():

    partidaEnMarcha = False
    maxpuntos = 160
    puntos = 0
    partidaEnMarcha = True

    while partidaEnMarcha:

        imagenTextoPuntos = letra30.render('Puntaje Maximo: ' + str (maxpuntos),
        True, (200,200,200), (0,0,0) )
        rectanguloTextoPuntos = imagenTextoPuntos.get_rect()
        rectanguloTextoPuntos.centerx = pantalla.get_rect().centerx
        rectanguloTextoPuntos.centery = 520

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit
                pygame.display.update()

        if puntos > maxpuntos:
            maxpuntos = puntos


        # ---- Presentacion ----
        pantalla.fill( (0,0,0) )
        pantalla.blit(imagenPresent, rectanguloPresent)
        pantalla.blit(imagenTextoPresent, rectanguloTextoPresent)
        pygame.display.flip()

        entrarAlMenu = False
        while not entrarAlMenu :
            pygame.time.wait(100)
            for event in pygame.event.get(KEYUP):
                if event.key == K_SPACE:
                    entrarAlMenu = True

        while entrarAlMenu:
            pantalla.fill( (0,0,0) )
            pantalla.blit(imagenMenu, rectanguloMenu)
            pantalla.blit(imagenTextoPuntos, rectanguloTextoPuntos)
            pygame.display.flip()


            entrarAlJuego = False
            while not entrarAlJuego:
                pygame.time.wait(100)
                for event in pygame.event.get(KEYUP):
                    if event.key == K_1:
                        entrarAlJuego = True
                    if event.key == K_2:
                        entrarAlJuego = True
                    if event.key == K_3:
                        mostrarCreditos = True
                        while mostrarCreditos:
                            pantalla.fill( (0,0,0) )
                            pantalla.blit(imagenCreditos, rectanguloCreditos)
                            pygame.display.flip()
                            for event in pygame.event.get(KEYUP):
                                if event.key == K_SPACE:
                                    completo()
                                    mostrarCreditos = False

            # COMIENZO DE LA PARTIDA----
            puntos = 0
            rectanguloLadron.left = ancho/2
            rectanguloLadron.top = alto-50
            rectanguloPatrullero.top = 20

            for i in range(0,cantidadPolicias+1):
                rectangulosPolicias[i] = imagenPolicia.get_rect()
                rectangulosPolicias[i].left = random.randrange(50,751)
                rectangulosPolicias[i].top = random.randrange(10,301)
                PoliciasVisibles[i] = True
                velocidadesX[i] = 3
                velocidadesY[i] = 3

            disparoActivo = False
            patrulleroVisible = True
            terminado = False

            while not terminado:
                # ---- Comprobar acciones del usuario ----
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminado = True
                        partidaEnMarcha = False

                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    rectanguloLadron.left -= 8
                if keys[K_RIGHT]:
                    rectanguloLadron.left += 8
                if keys[K_SPACE] and not disparoActivo:
                    disparoActivo = True
                    rectanguloDisparo.left = rectanguloLadron.left + 18
                    rectanguloDisparo.top = rectanguloLadron.top - 25

                # ---- Actualizar estado ----
                for i in range(0,cantidadPolicias+1):
                    rectangulosPolicias[i].left += velocidadesX[i]
                    rectangulosPolicias[i].top += velocidadesY[i]
                    if rectangulosPolicias[i].left < 0 or rectangulosPolicias[i].right > ancho:
                        velocidadesX[i] = -velocidadesX[i]
                    if rectangulosPolicias[i].top < 0 or rectangulosPolicias[i].bottom > alto:
                        velocidadesY[i] = -velocidadesY[i]

                rectanguloPatrullero.left += 2
                if rectanguloPatrullero.right > ancho:
                    rectanguloPatrullero.left = 0

                if disparoActivo:
                    rectanguloDisparo.top -= 6
                    if rectanguloDisparo.top <= 0:
                        disparoActivo = False

                # ---- Comprobar explosion
                for i in range(0,cantidadPolicias+1):
                    if PoliciasVisibles[i]:
                        if rectanguloLadron.colliderect( rectangulosPolicias[i] ):
                            terminado = True
                            if puntos > maxpuntos :
                                maxpuntos == puntos

                        if disparoActivo:
                            if rectanguloDisparo.colliderect( rectangulosPolicias[i]) :
                                PoliciasVisibles[i] = False
                                disparoActivo = False
                                puntos += 10

                if disparoActivo:
                    if rectanguloDisparo.colliderect( rectanguloPatrullero) :
                        patrulleroVisible = False
                        disparoActivo = False
                        puntos += 50

                cantidadPoliciasVisibles = 0
                for i in range(0,cantidadPolicias+1):
                    if PoliciasVisibles[i]:
                        cantidadPoliciasVisibles = cantidadPoliciasVisibles + 1

                if not patrulleroVisible and cantidadPoliciasVisibles == 0:
                    terminado = True
                    if puntos > maxpuntos:
                        maxpuntos == puntos

                # ---- Dibujar elementos en pantalla ----
                pantalla.fill( (0,0,0) )
                for i in range(0,cantidadPolicias+1):
                    if PoliciasVisibles[i]:
                        pantalla.blit(imagenPolicia, rectangulosPolicias[i])
                if patrulleroVisible:
                    pantalla.blit(imagenPatrullero, rectanguloPatrullero)
                if disparoActivo:
                    pantalla.blit(imagenDisparo, rectanguloDisparo)
                pantalla.blit(imagenLadron, rectanguloLadron)

                imagenPuntos = letra18.render('Puntos '+str(puntos),
                    True, (200,200,200), (0,0,0) )
                rectanguloPuntos = imagenPuntos.get_rect()
                rectanguloPuntos.left = 10
                rectanguloPuntos.top = 10
                pantalla.blit(imagenPuntos, rectanguloPuntos)
                if puntos >= maxpuntos:
                    maxpuntos = puntos

                pygame.display.flip()

                # ---- Ralentizar hasta 40 fotogramas por segundo  ----
                reloj.tick(50)  # 50 fps

        # ---- Final de partida ----
        pygame.quit()
completo()


