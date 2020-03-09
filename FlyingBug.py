import pygame
from pygame import mixer
import random
import math

pygame.init()
game_state = "start"

screen = pygame.display.set_mode((800,1280))

# Background
background = pygame.image.load('images/map.png')

# BGM
mixer.music.load('sound/space.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("FlyingBug")
icon = pygame.image.load('images/11B.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/player.PNG')
playerX = 350
playerY = 900
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/8B.PNG'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(4)
    enemyY_change.append(80)

# Bullet
bulletImg = pygame.image.load('images/MegaLaser.png')
bulletX = 0
bulletY = 900
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game Over text
GV_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True,(255,0,255))
    screen.blit(score, (x,y))

def game_over_text():
    game_over_text = GV_font.render("Game Over",True,(255,0,255))
    screen.blit(game_over_text, (250,350))
    

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 65, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 100:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # Screen
    screen.fill((0,0,0))
    # Backgound Map
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            print("A keystoke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if game_state is "over":
                    pygame.init()
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('sound/laser.wav')
                    bullet_sound.play()
                    # Get the current x cordinate 
                    bulletX = playerX
                    fire_bullet(playerX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0        

    playerX += playerX_change
           
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement 
    for i in range(num_of_enemies):

        # Game_over
        if enemyY[i] > 750:
            #game_over_sound = mixer.Sound('sound/game_over.wav')
            #game_over_sound.play(0)
            mixer.music.stop()
            
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_state = "over"
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]  
    
        # Collsion
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound = mixer.Sound('sound/explosion.wav')
            collision_sound.play()
            bulletY = 900
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(20, 100)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 900
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()