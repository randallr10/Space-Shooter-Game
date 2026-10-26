#import the pygame library 
import pygame 
import random
import requests
import sqlite3

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


#draws all aspects in the leaderboard game state; shows the top 5 highest scores in decending order.
def leaderboard():
  exitFont = pygame.font.Font(None, 50)
  text = exitFont.render("Esc to Exit", True, WHITE)
  screen.blit(text, (0,0))

  returnFont = pygame.font.Font(None, 50)
  text = returnFont.render("Backspace to Return", True, WHITE)
  screen.blit(text, (0,50))


  connect = sqlite3.connect('leaderboard.db')
  cursor = connect.cursor()
  cursor.execute('SELECT username, scores FROM SCORES ORDER BY CAST(scores AS INTEGER) DESC LIMIT 5')

  data = cursor.fetchall()

  connect.close()

  titleFont = pygame.font.Font(None, 100)
  dataFont = pygame.font.Font(None, 50)

  y=200

  title = titleFont.render("Leaderboard", True, WHITE)
  screen.blit(title, (600,100))

  for row in data:
    name = row[0]
    score = row[1]

    text = dataFont.render(str(name) + " - " + str(score), True, WHITE)
    screen.blit(text, (675, y))
    y+=100


#draws every aspect in the menu game state

def draw_menu():
  titleFont = pygame.font.Font(None, 100)
  text = titleFont.render("Space Shooter", True, WHITE)
  screen.blit(text, (525,500))

  startButFont = pygame.font.Font(None, 64)
  text = startButFont.render("Press down arrow to Start", True, WHITE)
  screen.blit(text, (490, 600))

  exitFont = pygame.font.Font(None, 50)
  text = exitFont.render("Esc to Exit", True, WHITE)
  screen.blit(text, (0,0))

  lbInstFont = pygame.font.Font(None, 50)
  text = lbInstFont.render("Press Num Pad Enter to see Leaderboard", True, WHITE)
  screen.blit(text, (450, 700))


#draws every aspect in the end screen game state

def draw_end(score):
  font = pygame.font.Font(None, 100)
  text = font.render("Defeated...", True, RED)
  screen.blit(text, (575,500))

  font = pygame.font.Font(None, 64)
  text = font.render("Press down arrow to Restart", True, WHITE)
  screen.blit(text, (425, 600))

  font = pygame.font.Font(None, 120)
  text = font.render("Score: " + str(score), True, YELLOW)
  screen.blit(text, (525,375))
  
  font = pygame.font.Font(None, 50)
  text = font.render("Press Num Pad enter to submit", True, WHITE)
  screen.blit(text, (450,650))

  exitFont = pygame.font.Font(None, 50)
  text = exitFont.render("Esc to Exit", True, WHITE)
  screen.blit(text, (0,0))

  return score


#submit score information function

def draw_submitScore(score, username):
  subScoreFont = pygame.font.Font(None, 50)
  text = subScoreFont.render("Submit score: " + str(score) + " as " + username, True, WHITE)
  screen.blit(text, (500,450))

  subInstrFont = pygame.font.Font(None, 50)
  text = subInstrFont.render("Press enter to submit", True, WHITE)
  screen.blit(text, (525,500))


#CREATE FUNCTIONS

#play functions
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



#DRWAING FUNCTIONS

  #draws the player character
def draw_player(player_x):
  player = pygame.Rect(player_x, 850, 50, 50)
  pygame.draw.rect(screen, WHITE, player)
  return player

#draws the billets onto the screen based on the coordinate they were created on.
def draw_bullets(bullets):
  for bullet in bullets:
    pygame.draw.rect(screen, YELLOW, bullet)

#draws the enemies to the screen based on random x and y coordinates from the created enemy in the list enemies.
def draw_enemies(enemies):
  for enemy in enemies:
    pygame.draw.rect(screen, RED, enemy)

#draws the score to the top of the screen and increases throughout the game
def draw_score(score):
  font = pygame.font.Font(None, 50)
  text = font.render("Score: " + str(score), True, WHITE)
  screen.blit(text, (0,0))
  return score

#draws the health you have left at the bottom of the screen
def draw_health(hitPoints):
  font = pygame.font.Font(None, 50)
  text = font.render("HP: " + str(hitPoints), True, WHITE)
  screen.blit(text, (725,950))
  return hitPoints



#MOVING FUNCTIONS

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
def move_enemies(enemies, bullets, score, hitPoints, player):
  speed = 1
  for enemy in enemies[:]:
    enemy.y += speed

    if enemy.top > 1000:
        enemies.remove(enemy)
        hitPoints -= 1
        continue

    if enemy.colliderect(player):
        enemies.remove(enemy)
        hitPoints -= 1
        continue

    for bullet in bullets[:]:
      if enemy.colliderect(bullet):
        enemies.remove(enemy)
        bullets.remove(bullet)
        score += 100
        break

  return score, hitPoints

 
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

    draw_menu()


  elif gameState == "leaderboard":
    if event.type == pygame.KEYDOWN:
      #exits the game loop and ends the program
      if event.key == pygame.K_ESCAPE:
        keep_playing = False
      #changes the game state back to the menu screen
      if event.key == pygame.K_BACKSPACE:
        gameState = "menu"
    screen.fill((0,0,0))

    leaderboard()
  
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
          bullets = create_bullet(bullets, player_x, bullet_y)
          last_shot = current_time   
    #checks for keyboard input
    keys = pygame.key.get_pressed()

    enemy_time = pygame.time.get_ticks()
    if enemy_time - last_enemy >= ENEMY_DELAY:
      #creates an enemy in the enemies list based on the players y value and a random x value
      enemies = create_enemies(enemies, enemy_y)
      last_enemy = enemy_time



    move_bullets(bullets, enemies)
    for bullet in bullets:
      pygame.draw.rect(screen, YELLOW, bullet)

    screen.fill((0,0,0))

    player_x = move_player(player_x)


    screen.fill((0, 0, 0))


    player = draw_player(player_x)

    score, hitPoints = move_enemies(enemies, bullets, score, hitPoints, player)
    if hitPoints == 0:
      gameState = "end"



    draw_bullets(bullets)

    draw_score(score)
    draw_health(hitPoints)

    draw_enemies(enemies)


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
    draw_end(score)

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
    draw_submitScore(score, username)


  #This function call updates the screen 
  pygame.display.update() 
  #sets the frame rate
  clock.tick(60) 


#quits the pygame module 
pygame.quit()
quit()