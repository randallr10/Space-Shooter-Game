#import the pygame library 
import pygame 
import random

#anchor the pygame screen so you see it in codio.
#Click on the arrow in the upper left corner to display in a new browser tab.
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

#start the pygame module 
pygame.init() 

#variables for screen size: 
screen_width=1500
screen_height=1000

#color code constants 
WHITE = (255,255,255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

#other variables & functions
player_x = 750
bullet_y = 875
enemy_y = 0
SHOT_DELAY = 350
ENEMY_DELAY = 1000
last_shot = 0
last_enemy = 0
bullets = []
enemies = []



#creates the bullets and their coordinates
def create_bullet(bullets, player_x, bullet_y):
  player_x = player_x + 20
  ammo = pygame.Rect(player_x, bullet_y, 10, 25)
  bullets.append(ammo)
  return bullets

#creates the enemies and adds them to a list
def create_enemies(enemies, enemy_y):
  enemy_x = random.randint(0, 1450)
  enemy = pygame.Rect(enemy_x, enemy_y, 50, 50)
  enemies.append(enemy)
  return enemies


  #draws the player character
def draw_player(player_x):
  pygame.draw.rect(screen, WHITE, (player_x, 900, 50, 50))

#draws the billets onto the screen based on the coordinate they were created on.
def draw_bullets(bullets):
  for bullet in bullets:
    pygame.draw.rect(screen, YELLOW, bullet)

def draw_enemies(enemies):
  for enemy in enemies:
    pygame.draw.rect(screen, RED, enemy)

#moves the player left and right without going off screen
def move_player(player_x):
  speed = 7.5
  if keys[pygame.K_LEFT]:
    if player_x > 0:
      player_x -= speed
  if keys[pygame.K_RIGHT]:
    if player_x < 1450:
      player_x += speed
  return player_x

#moves the bullets from the players location to the top of the screen and deletes it from the list once it reaches the top
def move_bullets(bullets, enemies):
  speed = 10
  for bullet in bullets:
    bullet.y -= speed
    if bullet.bottom < 0:
      bullets.remove(bullet)

#moves the enemies down towards the player
def move_enemies(enemies, bullets):
  speed = 1
  for enemy in enemies:
    enemy.y += speed
    for bullet in bullets:
      if enemy.top > 1000 or enemy.colliderect(bullet):
        enemies.remove(enemy)
        bullets.remove(bullet)



#create a screen with dimensions 
screen = pygame.display.set_mode((screen_width, screen_height)) 

#set the screen caption 
pygame.display.set_caption("Space Shooter")
screen.fill((0, 0, 0))

#the clock will be used to regulate the frame rate 
clock = pygame.time.Clock() 

#This function call updates the screen 
pygame.display.update() 

#sets the frame rate
clock.tick(60) 

#variable to control the game loop 
keep_playing=True 

#Game Loop - needed to keep updating and redrawing the screen 
while keep_playing==True: 
  #iterates over the current list of events(checks for events)  
  for event in pygame.event.get(): 
    #will stop the game loop if escape is pressed 
    if event.type == pygame.QUIT: 
      keep_playing = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot >= SHOT_DELAY:
          bullets = create_bullet(bullets, player_x, bullet_y)
          last_shot = current_time

          
  #checks for keyboard input
  keys = pygame.key.get_pressed()

  enemy_time = pygame.time.get_ticks()
  if enemy_time - last_enemy >= ENEMY_DELAY:
    enemies = create_enemies(enemies, enemy_y)
    last_enemy = enemy_time

  move_bullets(bullets, enemies)
  for bullet in bullets:
    pygame.draw.rect(screen, YELLOW, bullet)


  screen.fill((0,0,0))


  player_x = move_player(player_x)

  move_enemies(enemies, bullets)

  screen.fill((0, 0, 0))


  draw_bullets(bullets)
  
  draw_player(player_x)

  draw_enemies(enemies)

  #This function call updates the screen 
  pygame.display.update() 
  #sets the frame rate
  clock.tick(60) 

#quits the pygame module 
pygame.quit()
quit()