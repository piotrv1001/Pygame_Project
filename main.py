from collections import namedtuple
import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame project")

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
SPACE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
scaled_x = 41.3
scaled_y = 50
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (scaled_x, scaled_y)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (scaled_x, scaled_y)), -90)
YELLOW_INITIAL_POS = (100, HEIGHT / 2 - scaled_y / 2)
RED_INITIAL_POS = (WIDTH - 100 - scaled_x, HEIGHT / 2 - scaled_y / 2)

def draw_window(window, player1, player2, player1_bullets, player2_bullets, player1_health, player2_health):

    window.blit(SPACE_IMAGE, (0, 0))
    pygame.draw.rect(window, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render("Health: {health}".format(health = player1_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: {health}".format(health = player2_health), 1, WHITE)
    window.blit(yellow_health_text, (10, 10))
    window.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    window.blit(YELLOW_SPACESHIP, (player1.x, player1.y))
    window.blit(RED_SPACESHIP, (player2.x, player2.y))

    for bullet in player1_bullets:
        pygame.draw.rect(window, YELLOW, bullet)
    for bullet in player2_bullets:
        pygame.draw.rect(window, RED, bullet)

    pygame.display.update()

def handle_player_movement(keys_pressed, player, keys, startX, endX):

    # LEFT KEY
    if keys_pressed[keys.LEFT] and player.x - VELOCITY > startX:
        player.x -= VELOCITY
    # RIGHT KEY
    if keys_pressed[keys.RIGHT] and player.x + scaled_x + VELOCITY < endX:
        player.x += VELOCITY
    # TOP KEY
    if keys_pressed[keys.TOP] and player.y - VELOCITY > 0:
        player.y -= VELOCITY
    # BOTTOM KEY
    if keys_pressed[keys.BOTTOM] and player.y + scaled_y + VELOCITY < HEIGHT:
        player.y += VELOCITY

def handle_bullets(player1_bullets, player2_bullets, player1, player2):

    for bullet in player1_bullets:
        bullet.x += BULLET_VELOCITY
        if player2.colliderect(bullet):
            player1_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x + 10 >= WIDTH:
            player1_bullets.remove(bullet)

    for bullet in player2_bullets:
        bullet.x -= BULLET_VELOCITY
        if player1.colliderect(bullet):
            player2_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x <= 0:
            player2_bullets.remove(bullet)

def draw_winner(window, text):

    winner_text = WINNER_FONT.render(text, 1, WHITE)
    window.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    pygame.init()
    yellow = pygame.Rect(YELLOW_INITIAL_POS[0], YELLOW_INITIAL_POS[1], scaled_x, scaled_y)
    red = pygame.Rect(RED_INITIAL_POS[0], RED_INITIAL_POS[1], scaled_x, scaled_y)
    clock = pygame.time.Clock()

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    run = True

    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run  = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 3, 10, 6)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 3, 10, 6)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        Keys = namedtuple('Keys','TOP LEFT BOTTOM RIGHT')
        yellow_keys = Keys(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)
        red_keys = Keys(pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT)

        handle_player_movement(keys_pressed, yellow, yellow_keys, 0, WIDTH / 2 - 5)
        handle_player_movement(keys_pressed, red, red_keys, WIDTH / 2 + 5, WIDTH)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(WIN, yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(WIN, winner_text)
            break

    pygame.quit()

if __name__ == "__main__":
    main()