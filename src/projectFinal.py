import pygame 
import time
import random


width, height = 960, 960
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Don't Die")
back_ground = pygame.image.load("spaceBackground.jpg")
player_width = 40
player_height = 60
player_velocity = 5

def draw(player):
    win.blit(back_ground, (0, 0))
    pygame.draw.rect(win, "white", player)
    pygame.display.update()


####main game loop
def main():
    run = True

    player = pygame.Rect((width/2), height - player_height, 
                         player_width, player_height)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity >= 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.width <= width:
            player.x += player_velocity

        draw(player)

    pygame.quit()


if __name__ == "__main__":
     main()