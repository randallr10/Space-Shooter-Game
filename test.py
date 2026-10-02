import pygame

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Text Input")

font = pygame.font.Font(None, 40)

text = ""
input_box = pygame.Rect(100, 150, 400, 50)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # When the user types
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]

            elif event.key == pygame.K_RETURN:
                print("You entered:", text)

            else:
                text += event.unicode

    screen.fill((30, 30, 30))

    # Draw the text box
    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

    # Draw the text inside it
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

    pygame.display.update()

pygame.quit()