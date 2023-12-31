import pygame 
import time
import random
import os
from os import path


pygame.font.init()
pygame.mixer.init()

font = pygame.font.SysFont("ariel", 50)
width, height = 960, 960
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Don't Die")
back_ground = pygame.image.load("spaceBackground.jpg")
player_ship = pygame.image.load("spaceship.png")
shooting_star = pygame.image.load("shootingstar.png")
laser_img = pygame.image.load("laser_shot.png")

player_width = 40
player_height = 60
player_velocity = 5

star_width = 10
star_height = 20
star_velocity = 3

laser_width = 20
laser_height = 40
laser_velocity = 7

lives = 3
highscore_file = 'highscore.txt'

def draw(player, elapsed_time, stars, health, highscore, lasers, 
         laser_delete, ammo):
    win.blit(back_ground, (0, 0))

    time_text = font.render(f"Time: {round(elapsed_time)}s",
                             1, (153, 185, 255))
    win.blit(time_text, (10, 10))
    lives_text = font.render(f"Lives: {health}", 1,(61, 210, 255))
    win.blit(lives_text,(10, 50))
    highscore_text = font.render(f"Best Time: {highscore}s", 1, (61, 210, 255))
    win.blit(highscore_text, (10, height - 40)) 
    ammo_text = font.render(f"Ammo: {ammo}", 1,(61, 210, 255))
    win.blit(ammo_text, (10, 90))

    if laser_delete == False:
        for laser in lasers:
            win.blit(laser_img, laser)

    win.blit(player_ship, player)

    for star in stars:
        win.blit(shooting_star, star)

    pygame.display.update()


####main game loop
def main():
    with open(os.path.join(highscore_file), 'r') as file:
        highscore = int(file.read())


    music = pygame.mixer.music.load(os.path.join('gameMusic.mp3'))
    pygame.mixer.music.play(-1)

    pressed = False

    run = True

    player = pygame.Rect((width/2), height - player_height, 
                         player_width, player_height)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    lasers = []
    stars = []
    health = lives

    laser_count = 0
    laser_add_increment = 4000
    laser_delete = False
    ammo = 3

    while run:
        star_count += clock.tick(60)
        elapsed_time = int(time.time() - start_time)


        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, width - star_width)
                star = pygame.Rect(star_x, -star_height, 
                                   star_width, star_height)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 40)
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
        if keys[pygame.K_UP] and player.y - player_velocity >= 0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_height + player_velocity <= height:
            player.y += player_velocity
        
#---------------------------------------------------------
        laser_count += 12
        if laser_count > laser_add_increment and ammo > 0:

            if keys[pygame.K_SPACE]:
                laser = pygame.Rect((player.x + (player.width/2) - 
                                    (laser_width/2)), (player.y - 3), 
                                    laser_width, laser_height)
                ammo -= 1
                lasers.append(laser)
                pressed = True
                laser_delete = False
                laser_count = 0

        if pressed == True:

            for star in stars[:]:

                laser.y -= laser_velocity
                if laser.y + laser_height <= 0:
                    laser_delete = True
                    del laser
                    pressed = False
                    break                        
                elif pygame.Rect.colliderect(laser, star):
                    print('before star delete')
                    laser_delete = True
                    del laser
                    stars.remove(star)
                    pressed = False
                    break
                    

        for star in stars[:]:
            star.y += star_velocity
            if star.y > height:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                health -= 1
                break


        if health == 0:
            if elapsed_time > highscore:
                lost_text = font.render("New Highscore!", 1, "white")
            else:
                lost_text = font.render("You Lost!", 1, "white")
            
            win.blit(lost_text, (width/2 - lost_text.get_width()/2,
                                  height/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars, health, highscore, lasers, 
             laser_delete, ammo)

    if elapsed_time > highscore:
        highscore = elapsed_time
        with open('highscore.txt', 'w') as file:
            file.write(str(elapsed_time))

    pygame.quit()


if __name__ == "__main__":
     main()