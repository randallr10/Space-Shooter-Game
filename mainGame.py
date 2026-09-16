#import the pygame library 
import pygame 

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

#other variables & function
player_x = 750
bullet_y = 600
bullets = []

def create_bullet(bullets, player_x, bullet_y):
  ammo = (player_x, bullet_y, 10, 25)
  bullets.append(ammo)
  print(bullets)
  return bullets

def draw_bullets(bullets):
  for bullet in bullets:
    pygame.draw.rect(screen, YELLOW, bullet)
        
def move_player(player_x):
  speed = 5
  if keys[pygame.K_LEFT]:
    if player_x > 0:
      player_x -= speed
  if keys[pygame.K_RIGHT]:
    if player_x < 1450:
      player_x += speed
  return player_x

def draw_player(player_x):
  pygame.draw.rect(screen, WHITE, (player_x, 900, 50, 50))

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
        bullets = create_bullet(bullets, player_x, bullet_y)
  

  #checks for keyboard input
  keys = pygame.key.get_pressed()


  screen.fill((0,0,0))
  player_x = move_player(player_x)

  screen.fill((0, 0, 0))

  draw_bullets(bullets)
  
  draw_player(player_x)
       
  #This function call updates the screen 
  pygame.display.update() 
  #sets the frame rate
  clock.tick(60) 

#quits the pygame module 
pygame.quit()
quit()