import pygame
from pygame import mixer
from tkinter import *
from tkinter import messagebox

pygame.init()
mixer.init()
mixer.music.load("Games\Star Warriors\Assets\ibg_music.mp3")
mixer.music.play(5)

WIDTH, HEIGHT = 900, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Antariksh Yodha")
win_IMG = pygame.display.set_icon(pygame.image.load('Games\Star Warriors\Assets\Logo.png'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Games\Star Warriors\Assets\Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Games\Star Warriors\Assets\Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('Times New Roman', 40)
winNER_FONT = pygame.font.SysFont('Times New Roman', 70, 'Bold')

FPS = 60
VEL = 5
BULLET_VEL = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 55
A_SPACESHIP_WIDTH, A_SPACESHIP_HEIGHT = 100, 85

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load('Games\Star Warriors\Assets\spaceship_red.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)

RED_SPACESHIP_IMAGE = pygame.image.load('Games\Star Warriors\Assets\spaceship_yellow.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (A_SPACESHIP_WIDTH, A_SPACESHIP_HEIGHT)), 0)

SPACE = pygame.transform.scale(pygame.image.load('Games\Star Warriors\Assets\Space.jpg'), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    '''animation = True
    i = 0
    list = []
    while animation:
        if i < 63:
            image = pygame.transform.scale(pygame.image.load(f'C:\shivansh_python\Games\Star Warriors\Assets\Intro_ani\{i}.jpg'), (WIDTH, HEIGHT))
            win.blit(image, (0, 0))
            list.append(image)
            i = i + 1'''
    win.blit(SPACE, (0, 0))
    pygame.draw.rect(win, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, GREEN)
    win.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))

    win.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    win.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(win, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(win, GREEN, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = winNER_FONT.render(text, 1, WHITE)
    win.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def message_box(subject, content):
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 100
    yellow_health = 100

    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_ESCAPE:
                    run = False
                    message_box('Special Credits',
               '''S△Ms (Samarthya) Productions-Indian Baja(Intro Track)
               S△Ms (Samarthya) Productions-Indian Baja(Title Track)
               Assets by Samarthya''')
                    break

            if event.type == RED_HIT:
                red_health -= 2
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 2
                BULLET_HIT_SOUND.play()
                
                

        winner_text = ""
        if red_health <= 0:
            winner_text = "X wing wins!"

        if yellow_health <= 0:
            winner_text = "Millennium Falcon wins!"

        if winner_text != "":
            draw_winner(winner_text)
            run = False

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)
        
    pygame.display.update()
main()