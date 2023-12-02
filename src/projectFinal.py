import pygame 
import time
import random


pygame.font.init()
font = pygame.font.SysFont("ariel", 30)
width, height = 960, 960
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Don't Die")
back_ground = pygame.image.load("spaceBackground.jpg")

player_width = 40
player_height = 60
player_velocity = 5

star_width = 10
star_height = 20
hit = False
star_velocity = 3

def draw(player, elapsed_time, stars):
    win.blit(back_ground, (0, 0))

    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "white")
    win.blit(time_text, (10, 10))

    pygame.draw.rect(win, "white", player)

    for star in stars:
        pygame.draw.rect(win, "white", star)

    pygame.display.update()



####main game loop
def main():
    run = True

    player = pygame.Rect((width/2), height - player_height, 
                         player_width, player_height)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars= []

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, width - star_width)
                star = pygame.Rect(star_x, -star_height, 
                                   star_width, star_height)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity >= 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.width <= width:
            player.x += player_velocity

        for star in stars[:]:
            star.y += star_velocity
            if star.y > height:
                stars.remove(star)
            elif star.y + star.height>= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break


        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
     main()