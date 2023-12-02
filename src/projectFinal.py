import pygame 
import time
import random


width, height = 960, 960
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Don't Die")
back_ground = pygame.image.load("spaceBackground.jpg")
player_width = 40
player_height = 60


def draw(player):
    win.blit(back_ground, (0, 0))
    pygame.draw.rect(win, "white", player)
    pygame.display.update()


####main game loop
def main():
    run = True

    player = pygame.Rect(200, height - player_height, 
                         player_width, player_height)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(player)

    pygame.quit()


if __name__ == "__main__":
     main()