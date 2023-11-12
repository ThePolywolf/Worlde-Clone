import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display (window)
screen_width = 400
screen_height = 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minimal Enter Key Test")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if a key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                print("Enter Key Pressed")

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()