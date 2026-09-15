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

#other variable initializers (fonts, text, images, etc)
player_x = 750
speed = 5

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

  keys = pygame.key.get_pressed()

  if keys[pygame.K_LEFT]:
    if player_x > 0:
      player_x -= speed
  if keys[pygame.K_RIGHT]:
    if player_x < 1450:
      player_x += speed

  screen.fill((0, 0, 0))

  pygame.draw.rect(screen, WHITE, (player_x, 900, 50, 50))

       
  #This function call updates the screen 
  pygame.display.update() 
  #sets the frame rate
  clock.tick(60) 

#quits the pygame module 
pygame.quit() 
quit() 