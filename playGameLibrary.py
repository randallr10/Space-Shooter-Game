import pygame
import random

WHITE = (255,255,255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

screen_width=1500
screen_height=1000
screen = pygame.display.set_mode((screen_width, screen_height))

class DrawGame:
    #draws the player character
    def drawPlayer(player_x):
        player = pygame.Rect(player_x, 850, 50, 50)
        pygame.draw.rect(screen, WHITE, player)
        return player

    #draws the health you have left at the bottom of the screen
    def drawHealth(hitPoints):
        font = pygame.font.Font(None, 50)
        text = font.render("HP: " + str(hitPoints), True, WHITE)
        screen.blit(text, (725,950))
        return hitPoints
    
    #draws the score to the top of the screen and increases throughout the game
    def drawScore(score):
        font = pygame.font.Font(None, 50)
        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (0,0))
        return score

    #draws the enemies to the screen based on random x and y coordinates from the created enemy in the list enemies.
    def drawEnemies(enemies):
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

    #draws the billets onto the screen based on the coordinate they were created on.
    def drawBullets(bullets):
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)


class CreateGameElements:
    #creates the bullets and their coordinates
    def createBullet(bullets, player_x, bullet_y):
        player_x = player_x + 20
        ammo = pygame.Rect(player_x, bullet_y, 10, 25)
        bullets.append(ammo)
        return bullets

    #creates the enemies and adds them to a list
    def createEnemies(enemies, enemy_y):
        enemy_x = random.randint(0, 1450)
        enemy = pygame.Rect(enemy_x, enemy_y, 50, 50)
        enemies.append(enemy)
        return enemies

class MoveElements:
    #moves the player left and right without going off screen
    def movePlayer(player_x):
        keys = pygame.key.get_pressed()
        speed = 7.5
        if keys[pygame.K_LEFT]:
            if player_x > 0:
                player_x -= speed
        if keys[pygame.K_RIGHT]:
            if player_x < 1450:
                player_x += speed
        return player_x

    #moves the bullets from the players location to the top of the screen and deletes it from the list once it reaches the top
    def moveBullets(bullets, enemies):
        speed = 10
        for bullet in bullets:
            bullet.y -= speed
            if bullet.bottom < 0:
                bullets.remove(bullet)
    
    #moves the enemies down towards the player
    def moveEnemies(enemies, bullets, score, hitPoints, player):
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