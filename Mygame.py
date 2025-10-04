import pygame
import pgzrun

# Tamaño del juego
size_w = 10
size_h = 10
WIDTH = size_w * 80
HEIGHT = size_h * 60

# Cargar imagen de fondo con pygame
original_image = pygame.image.load("background.png")
img_width, img_height = original_image.get_size()
scale = min(WIDTH / img_width, HEIGHT / img_height)
new_size = (int(img_width * scale), int(img_height * scale))
scaled_image = pygame.transform.scale(original_image, new_size)

# Centrar imagen
x = (WIDTH - new_size[0]) // 2
y = (HEIGHT - new_size[1]) // 2

# Variables de modo
mode = "menu"
key_collected = False

# Actores
button_play = Actor("button", (400, 300))
key = Actor("key")
key.pos = (500, 240)  # Posición visible sobre plataforma
platform = Actor("platform")
cavern = Actor("cavern_bg")
mujer = Actor("mujer", (600, 300))
nino = Actor("nino", (320, 300))

# Física
gravity = 1
jump_strengh = -15
nino.vy = 0
mujer.vx = 3
mujer.vy = 0

# Mapa
my_map = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2],
    [2, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 1:
                platform.left = platform.width * j
                platform.top = platform.height * i
                platform.draw()
            elif my_map[i][j] == 2:
                cavern.left = cavern.width * j
                cavern.top = cavern.height * i
                cavern.draw()

def draw():
    if mode == "menu":
        screen.blit(scaled_image, (x, y))
        button_play.draw()
        screen.draw.text("PLAY", center=button_play.pos, fontsize=30, color="black")
    elif mode == "game":
        screen.clear()
        screen.blit("bg", (0, 0))
        map_draw()
        mujer.draw()
        nino.draw()
        if not key_collected:
            key.draw()

def on_mouse_down(pos):
    global mode
    if mode == "menu":
        if button_play.collidepoint(pos):
            mode = "game"

def update():
    global key_collected

    if mode == "game":
        # Movimiento horizontal
        if keyboard.right:
            nino.x += 5
        if keyboard.left:
            nino.x -= 5

        # Salto con flecha arriba
        if keyboard.up and nino.vy == 0:
            nino.vy = jump_strengh

        # Gravedad
        nino.vy += gravity
        nino.y += nino.vy

        # Rectángulo del niño
        bunny_rect = Rect((nino.x - nino.width / 2, nino.y - nino.height / 2), (nino.width, nino.height))

        # Rectángulos de plataformas
        platform_rects = []
        for i in range(len(my_map)):
            for j in range(len(my_map[0])):
                if my_map[i][j] == 1:
                    plat_rect = Rect((j * platform.width, i * platform.height), (platform.width, platform.height))
                    platform_rects.append(plat_rect)

        # Colisión con plataformas
        for p_rect in platform_rects:
            if bunny_rect.colliderect(p_rect) and nino.vy >= 0:
                nino.y = p_rect.top - nino.height / 2
                nino.vy = 0

        # Movimiento de la mujer
        if nino.x > mujer.x:
            mujer.x += mujer.vx
        elif nino.x < mujer.x:
            mujer.x -= mujer.vx

        # Recoger la llave
        if not key_collected and nino.colliderect(key):
            key_collected = True
            print("¡Llave recogida!")

def on_key_down():
    if mode == "game":
        if keyboard.space and nino.vy == 0:
            nino.vy = jump_strengh

pgzrun.go()
