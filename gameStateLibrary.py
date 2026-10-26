import pygame
import sqlite3

WHITE = (255,255,255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

screen_width=1500
screen_height=1000
screen = pygame.display.set_mode((screen_width, screen_height))

class DrawStates:
    def drawLeaderboard():
        #draws all aspects in the leaderboard game state; shows the top 5 highest scores in decending order.
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

    def drawMenu():
        #draws every aspect in the menu game state
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

    def drawEnd(score):
        #draws every aspect in the end screen game state
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

    def drawSubScore(score, username):
        #submit score information function
        subScoreFont = pygame.font.Font(None, 50)
        text = subScoreFont.render("Submit score: " + str(score) + " as " + username, True, WHITE)
        screen.blit(text, (500,450))

        subInstrFont = pygame.font.Font(None, 50)
        text = subInstrFont.render("Press enter to submit", True, WHITE)
        screen.blit(text, (525,500))