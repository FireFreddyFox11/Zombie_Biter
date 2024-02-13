import pygame
from pygame import mixer
import random

pygame.init()

SCREEN_WIDTH = 530
SCREEN_HEIGHT = 530

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
game_cap = pygame.display.set_caption("Zombie Biter")

font = pygame.font.SysFont('Arial', 32)

fps = 60

text = font.render("Score: " + str(0), True, (47, 54, 153))

text_rect = text.get_rect()

Person = pygame.image.load("Person.png")
Zombie = pygame.image.load("Zombie.png")
Background = pygame.image.load("Arena.png")
tada = pygame.mixer.Sound("tada.mp3")
growl = pygame.mixer.Sound("Zombie_growl.mp3")

tada.set_volume(0.3)
growl.set_volume(0.6)

mixer.init(20000, -16, 1)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel1.play(growl, loops=-1)

Person_size = pygame.transform.scale(Person, (35, 60))
Zombie_size = pygame.transform.scale(Zombie, (35, 60))
Background_size = pygame.transform.scale(Background, (SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect(230, 340, 20, 25)

rand_x = random.randint(10, SCREEN_WIDTH-35)
rand_y = random.randint(10, SCREEN_HEIGHT)

enemy = pygame.Rect(rand_x, rand_y, 20, 25)
enemy2 = pygame.Rect(50, 50, 20, 25)

direction = [1, 1]
velocity_player = 4
velocity_enemy = 4


def draw_enemy(enemies, x, y):
    enemies = pygame.draw.rect(screen, (34, 177, 76), enemies)
    screen.blit(Zombie_size, enemies)
    enemies.x = x
    enemies.y = y
    pygame.display.update()

def reset(p, e, e2):
    p.x = 230
    p.y = 340
    e.x = random.randint(0, SCREEN_WIDTH-35)
    e.y = random.randint(0, SCREEN_HEIGHT-57)
    e2.x = random.randint(0, SCREEN_WIDTH-35)
    e2.y = random.randint(0, SCREEN_HEIGHT-57)
    if e.x == e2.x or e.y == e2.y or e.x >= p.x-20 or e.x <= p.x+20 or e.y >= p.y-20 or e.y <= p.y+20:
        e.x = random.randint(0, SCREEN_WIDTH-35)
        e.y = random.randint(0, SCREEN_HEIGHT-57)
        e2.x = random.randint(0, SCREEN_WIDTH-35)
        e2.y = random.randint(0, SCREEN_HEIGHT-57)
    channel1.play(growl, loops=-1)

def PSC(Proj):
    proj_x = direction[0] * velocity_enemy
    proj_y = direction[1] * velocity_enemy
    Proj.move_ip(proj_x, proj_y)

    if Proj.left < 20 or Proj.right > SCREEN_WIDTH-40:
        direction[0] *= -1
    if Proj.top < 20 or Proj.bottom > SCREEN_HEIGHT-60:
        direction[1] *= -1

def draw(player):
    # background
    screen.fill((255, 255, 255))
    screen.blit(Background_size, (0, 0))
    #entities
    player = pygame.draw.rect(screen, (34, 177, 76), player)
    screen.blit(Person_size, player)
    pygame.display.update()

def move_towards_player(enemy, player):
    dirvect = pygame.math.Vector2(player.x - enemy.x, player.y - enemy.y)
    dirvect.normalize()
    dirvect.scale_to_length(velocity_enemy)   
    enemy.move_ip(dirvect)

def main():
    Run = True
    clock = pygame.time.Clock()
    Score = 0
    inc = 1
    velocity_player = 4
    velocity_enemy = 4
    while Run:
        Score += 1
        if Score % 10 == 0:
            velocity_enemy += 0.01
            velocity_player += 0.01
            inc += 1
            if inc % 50 == 0:
                velocity_enemy += 0.02
        fps = clock.tick(60)
        draw(player) 
        draw_enemy(enemy, rand_x, rand_y)   
        draw_enemy(enemy2, 50, 50)
        PSC(enemy2)
        move_towards_player(enemy, player)
        
        text = font.render("Score: " + str('{0:.2f}'.format(Score)), True, (255, 255, 255))
        text_rect.center = (70, 35)
        screen.blit(text, text_rect)

        text_fps = font.render("FPS: " + str(60-fps), True, (255, 255, 255))
        text_fps_rect = text_fps.get_rect()
        text_fps_rect.center = (430, 35)
        screen.blit(text_fps, text_fps_rect)

        pygame.display.update()
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and player.left > 20:
            player.x -= velocity_player
        if key[pygame.K_d] and player.right < SCREEN_WIDTH-35:
            player.x += velocity_player
        if key[pygame.K_w] and player.top > 20:
            player.y -= velocity_player
        if key[pygame.K_s] and player.bottom < SCREEN_HEIGHT-57:
            player.y += velocity_player
        if pygame.Rect.colliderect(enemy, player) or pygame.Rect.colliderect(enemy2, player):
            channel1.stop()
            channel2.play(tada)

            text2 = font.render("Congrats! Your final score is " + str(Score), True, (255, 255, 255))
            text_rect2 = text.get_rect()
            text_rect2.center = (125, 100)
            screen.blit(text2, text_rect2)

            pygame.display.update()
            Score += -1
            pygame.time.delay(2000)
            reset(player, enemy, enemy2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                Run = False
                pygame.quit()
    main()

if __name__ == "__main__":
    main()
