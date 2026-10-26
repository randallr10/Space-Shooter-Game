#import the pygame library 
import pygame 
import random
import requests
import sqlite3
from gameStateLibrary import DrawStates
from playGameLibrary import DrawGame, CreateGameElements, MoveElements

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
bullet_y = 800
enemy_y = 0
SHOT_DELAY = 350
ENEMY_DELAY = 1250
last_shot = 0
last_enemy = 0
bullets = []
enemies = []
score = 0
hitPoints = 3
username = ""

#inputs the values username and score into a flask function to be inputed into a sql table
def save_score(username, score):
  url = 'http://10.30.1.20:5000/submit_score'

  data = {
    'username': username,
    'scores': score
  }
  
  response = requests.post(url, json = data)

  print(response.json())


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
gameState="menu"
name_confirmed = False

input_box = pygame.Rect(475, 300, 575, 100)

#Game Loop - needed to keep updating and redrawing the screen 
while keep_playing==True: 

  #iterates over the current list of events(checks for events)  
  for event in pygame.event.get(): 
    #will stop the game loop if escape is pressed 
    if event.type == pygame.QUIT: 
      keep_playing = False
    if event.type == pygame.KEYDOWN:
      #enters the username typed in as a confirmed name and if nothing is inserted when entered, its value is set to anonymous.
      if event.key == pygame.K_RETURN:
        if username.strip() != "":
          name_confirmed = True
        else:
          username = "Anonymous"
          name_confirmed = True
      
      #when backspace is hit the last character typed in is deleted from the username value.
      elif event.key == pygame.K_BACKSPACE:
        username = username[:-1]

      #this checks for any key press on your keyboard and adds that value onto the username value.
      else:
        if not name_confirmed and len(username) < 15:
          username += event.unicode

  if gameState == "menu":
    screen.fill((0,0,0))
    if event.type == pygame.KEYDOWN:
      #checks if the username is entered and changes the game state to play to start the game \ 
      #if the username is not entered it will not change
      if event.key == pygame.K_DOWN:
        if name_confirmed == True:
          gameState = "play"
      #exits the game loop and ends the program
      if event.key == pygame.K_ESCAPE:
        keep_playing = False
      #changes the game state to leaderboard when pressed
      if event.key == pygame.K_KP_ENTER:
        gameState = "leaderboard"

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 26)

    #removes the input username box when the name is entered
    if not name_confirmed:
        title = font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(title, (input_box.x, input_box.y - 50))

        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

        name_text = font.render(username, True, WHITE)
        screen.blit(name_text, (input_box.x + 10, input_box.y + 30))

    DrawStates.drawMenu()


  elif gameState == "leaderboard":
    if event.type == pygame.KEYDOWN:
      #exits the game loop and ends the program
      if event.key == pygame.K_ESCAPE:
        keep_playing = False
      #changes the game state back to the menu screen
      if event.key == pygame.K_BACKSPACE:
        gameState = "menu"
    screen.fill((0,0,0))

    DrawStates.drawLeaderboard()
  
  elif gameState == "play":
    screen.fill((0,0,0))
    if event.type == pygame.KEYDOWN:
      #ends the game loop and ends the program
      if event.key == pygame.K_ESCAPE:
        keep_playing = False

      if event.key == pygame.K_UP:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot >= SHOT_DELAY:
          #creates a bullet in the list bullets based on the players x and y value
          bullets = CreateGameElements.createBullet(bullets, player_x, bullet_y)
          last_shot = current_time

    enemy_time = pygame.time.get_ticks()
    if enemy_time - last_enemy >= ENEMY_DELAY:
      #creates an enemy in the enemies list based on the players y value and a random x value
      enemies = CreateGameElements.createEnemies(enemies, enemy_y)
      last_enemy = enemy_time

    MoveElements.moveBullets(bullets, enemies)
    for bullet in bullets:
      pygame.draw.rect(screen, YELLOW, bullet)

    screen.fill((0,0,0))

    player_x = MoveElements.movePlayer(player_x)


    screen.fill((0, 0, 0))


    player = DrawGame.drawPlayer(player_x)

    score, hitPoints = MoveElements.moveEnemies(enemies, bullets, score, hitPoints, player)
    if hitPoints == 0:
      gameState = "end"



    DrawGame.drawBullets(bullets)

    DrawGame.drawScore(score)
    DrawGame.drawHealth(hitPoints)

    DrawGame.drawEnemies(enemies)


  elif gameState == "end":
    if event.type == pygame.KEYDOWN:
      #ends the game loop and closes the program
      if event.key == pygame.K_ESCAPE:
        keep_playing = False
    if event.type == pygame.KEYDOWN:
      #sends the player to the submit game state where they can submit their score
      if event.key == pygame.K_KP_ENTER:
        gameState = "submit"
    screen.fill((0,0,0))
    if event.type == pygame.KEYDOWN:
      #when pressed, the player will get sent back to the game to re-try, all changeable values are also reset.
      if event.key == pygame.K_DOWN:
        gameState = "play"
        bullets = []
        enemies = []
        score = 0
        hitPoints = 3
        player_x = 750
        name_confirmed = False
    DrawStates.drawEnd(score)

  elif gameState == "submit":
    if event.type == pygame.KEYDOWN:
      #ends game loop and closes the program
      if event.key == pygame.K_ESCAPE:
        keep_playing = False
      #score is submited to flask and then into a sql table
      if event.key == pygame.K_RETURN:
        save_score(username, score)
        username = ""
        name_confirmed = False
        gameState="menu"
    screen.fill((0,0,0))
    DrawStates.drawSubScore(score, username)


  #This function call updates the screen 
  pygame.display.update() 
  #sets the frame rate
  clock.tick(60) 


#quits the pygame module 
pygame.quit()
quit()