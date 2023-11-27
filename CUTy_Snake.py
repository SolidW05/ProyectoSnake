import pygame
import random
import botones

pygame.init()

# *** ________ colores
color_fondo = (67, 89, 4)
color_serpiente = (168, 86, 76)
blanco = (255, 255, 255)
comida_e = (255,0,255)
rojo = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
negro = (0,0,0)
color_fondo2 = (202, 228, 241)

# *** ____________ Sonidos
yum = pygame.mixer.Sound("sonidos/yum.mp3")
yummy = pygame.mixer.Sound("sonidos/yummy.mp3")
yum.set_volume(200)
yummy.set_volume(200)


# Configuracion de la pantalla
ancho = 800
largo = 600
pantalla = pygame.display.set_mode((ancho, largo))
pygame.display.set_caption(f'CUTy Snake')

# *** Cargar imagenes
iniciar_imagen = pygame.image.load('imagenes/Iniciar.png').convert_alpha()
salir_imagen = pygame.image.load('imagenes/Salir.png').convert_alpha()
logo = pygame.image.load('imagenes/logo_trans.png').convert_alpha()
# *** ___________ Crear botones
iniciar_boton = botones.Button(230,125, iniciar_imagen, .8)
salir_boton = botones.Button(230, 300, salir_imagen, .8)
logo2 = botones.Button(220,50, logo, .2)
#cuerpo de la serpiente
cuerpo_S = 20

fps = pygame.time.Clock()

#configura el estilo del mensaje
mensaje_estilo = pygame.font.SysFont("comicssansms", 30)

def mensaje(msg, color,x, y):
    mesg = mensaje_estilo.render(msg, True, color)
    pantalla.blit(mesg, [x, y])

# pinta la serpiente
def serpiente(cuerpo_S, lista_s):
    for e in lista_s:
        pygame.draw.rect(pantalla, color_serpiente, [e[0], e[1], cuerpo_S, cuerpo_S])
# Crear botones


def Juego():
    x_inicio = round(random.randrange(0, ancho - cuerpo_S) / cuerpo_S) * cuerpo_S

    y_inicio = round(random.randrange(0, largo - cuerpo_S) / cuerpo_S) * cuerpo_S

    velocidad_Original_S = 5
    velocidad_S = velocidad_Original_S
    aumentoV = 25
    cambio_x = 0
    cambio_y = 0

    # aparicion de la comida
    comidax = round(random.randrange(0, ancho - cuerpo_S) / cuerpo_S) * cuerpo_S
    comiday = round(random.randrange(0, largo - cuerpo_S) / cuerpo_S) * cuerpo_S

    # aparicion de la comida especial
    x_5 = round(random.randrange(0, ancho - cuerpo_S) / cuerpo_S) * cuerpo_S
    y_5 = round(random.randrange(0, largo - cuerpo_S) / cuerpo_S) * cuerpo_S

    # Cronometro Comida especial
    tiempo_actual = 0
    primera_vuelta = 1
    tiempo_tras_comer = 0
    lista_s = []
    largo_s = 1

    jugando = True
    perdido = False

    while jugando:
        tiempo_actual = pygame.time.get_ticks()

        while perdido == True:
            puntaje = largo_s -1

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        jugando = False

            pantalla.fill(color_fondo2)

            if iniciar_boton.draw(pantalla):
                Juego()
            if salir_boton.draw(pantalla):
                perdido = False
                jugando = False
            mensaje(f"Has perdido, tu puntaje es {puntaje}",negro , 250,50)
            mensaje("#Controles:", negro, 250, 455)
            mensaje("shift izquierdo | Correr", negro, 250, 480)
            mensaje("WASD y flechas | Movimiento", negro, 250, 505)
            pygame.display.update()




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False

            tiempo_actual = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    cambio_x = -cuerpo_S
                    cambio_y = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    cambio_x = cuerpo_S
                    cambio_y = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    cambio_y = -cuerpo_S
                    cambio_x = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    cambio_y = cuerpo_S
                    cambio_x = 0
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RIGHT:
                    velocidad_S += aumentoV

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RIGHT:
                    velocidad_S = velocidad_Original_S

        # Si choca con los bordes se acaba el juego
        if (y_inicio >= largo or y_inicio < 0) or (x_inicio >= ancho or x_inicio < 0):
            perdido = True

        x_inicio += cambio_x
        y_inicio += cambio_y
        pantalla.fill(color_fondo)

        # *** ____________________ Renderizacion
        pygame.draw.rect(pantalla, rojo, [comidax, comiday, cuerpo_S, cuerpo_S])

        if tiempo_actual - tiempo_tras_comer > 30000 or primera_vuelta == 1:
            pygame.draw.rect(pantalla, comida_e, [x_5, y_5, cuerpo_S, cuerpo_S])

        cabeza_s = []
        cabeza_s.append(x_inicio)
        cabeza_s.append(y_inicio)
        lista_s.append(cabeza_s)
        if len(lista_s) > largo_s:
            del lista_s[0]

        for e in lista_s[:-1]:
            if e == cabeza_s:
                perdido = True

        serpiente(cuerpo_S, lista_s)
        pygame.display.update()

        if x_inicio == comidax and y_inicio == comiday:
            comidax = round(random.randrange(0, ancho - cuerpo_S) / cuerpo_S) * cuerpo_S
            comiday = round(random.randrange(0, largo - cuerpo_S) / cuerpo_S) * cuerpo_S
            yum.play()
            largo_s += 1

        if x_inicio == x_5 and y_inicio == y_5:
            largo_s += 15
            tiempo_tras_comer = pygame.time.get_ticks()
            primera_vuelta = 0
            yummy.play()
            x_5 = round(random.randrange(0, ancho - cuerpo_S) / cuerpo_S) * cuerpo_S
            y_5 = round(random.randrange(0, largo - cuerpo_S) / cuerpo_S) * cuerpo_S
        fps.tick(velocidad_S)
    pygame.quit()

def pantalla_inicio():

    menu = True
    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False


        pantalla.fill(color_fondo2)
        logo2.draw(pantalla)
        if iniciar_boton.draw(pantalla):
            Juego()
        if salir_boton.draw(pantalla):
            menu = False
        mensaje("#Controles:", negro, 250, 455)
        mensaje("shift izquierdo | Correr", negro, 250, 480)
        mensaje("WASD y flechas | Movimiento", negro, 250, 505)
        pygame.display.update()

pantalla_inicio()

