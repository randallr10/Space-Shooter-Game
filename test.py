
import pygame

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Name Input Example")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 26)

username = ""
name_confirmed = False
running = True

input_box = pygame.Rect(150, 160, 300, 50)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                if username.strip() != "":
                    name_confirmed = True

            elif event.key == pygame.K_BACKSPACE:
                username = username[:-1]

            else:
                if not name_confirmed and len(username) < 15:
                    if event.unicode.isprintable():
                        username += event.unicode

    screen.fill((20, 25, 45))

    if not name_confirmed:
        title = font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(title, (180, 100))

        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

        name_text = font.render(username, True, (100, 220, 255))
        screen.blit(name_text, (input_box.x + 10, input_box.y + 10))

        instructions = small_font.render(
            "Press ENTER to confirm", True, (200, 200, 200)
        )
        screen.blit(instructions, (185, 235))

    else:
        message = font.render(
            "Welcome, " + username + "!", True, (100, 255, 150)
        )
        screen.blit(message, (150, 170))

    pygame.display.update()

pygame.quit()
