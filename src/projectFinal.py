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

player_width = 40
player_height = 60
player_velocity = 5

star_width = 10
star_height = 20
star_velocity = 3

laser_width = 5
laser_height = 10
laser_velocity = 7

lives = 3
highscore_file = 'highscore.txt'

def draw(player, elapsed_time, stars, health, highscore, lasers):
    win.blit(back_ground, (0, 0))

    time_text = font.render(f"Time: {round(elapsed_time)}s",
                             1, (153, 185, 255))
    win.blit(time_text, (10, 10))
    lives_text = font.render(f"Lives: {health}", 1,(61, 210, 255))
    win.blit(lives_text,(10, 50))
    highscore_text = font.render(f"Best Time: {highscore}s", 1, (61, 210, 255))
    win.blit(highscore_text, (10, height - 40)) 

    for laser in lasers:
        pygame.draw.rect(win, 'white', laser)

    win.blit(player_ship, player)

    for star in stars:
        win.blit(shooting_star, star)

    pygame.display.update()

'''
def shoot(stars, player):
        laser = pygame.Rect((player.x + (player.width/2) - 
                             (laser_width/2)), (player.y - 3), 
                        laser_width, laser_height)

        #break_from_stars = False

        return laser
        while True:
            clock = pygame.time.Clock()
            clock.tick(2000)
            print('clock run')
            laser.y -= laser_velocity#cant be in this loop
            if laser.y < -height - laser_height:#cant be in this loop
                del laser
                break

            for star in stars[:]:
                #print('star')
                if laser.colliderect(star):

                    #star_loca = star
                    stars.remove(star)
                    del laser
                    break_from_stars = True
                    break

            if break_from_stars == True:
                break

        #win.blit(laser_img, laser)
            pygame.draw.rect(win, 'white', laser)#cant be in this loop
            pygame.display.update()
'''


####main game loop
def main():
    with open(os.path.join(highscore_file), 'r') as file:
        highscore = int(file.read())


    music = pygame.mixer.music.load(os.path.join('gameMusic.mp3'))
    pygame.mixer.music.play(-1)

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

    while run:
        star_count += clock.tick(60)
        elapsed_time = int(time.time() - start_time)
        print(star_count)

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, width - star_width)
                star = pygame.Rect(star_x, -star_height, 
                                   star_width, star_height)
                stars.append(star)

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
        if keys[pygame.K_UP] and player.y - player_velocity >= 0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_height + player_velocity <= height:
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            laser = pygame.Rect((player.x + (player.width/2) - 
                                 (laser_width/2)), (player.y - 3), 
                                 laser_width, laser_height)
            lasers.append(laser)



        for laser in lasers[:]:
            laser.y -= laser_velocity
            if laser.y < -height - laser_height:
                del laser
                print('laser delete')
            #elif laser.y + laser_height <= star.y and laser.colliderect(star):
            #    laser_hit = laser

            for star in stars[:]:
                if laser.y + laser_height <= star.y and laser.colliderect(star):
                    #laser_hit = laser
                    stars.remove(star)
                    del laser
       #             print('after star and laser delete')
       #             #break_from_stars = True
       #             break



        for star in stars[:]:
            star.y += star_velocity
            if star.y > height:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                health -= 1
                break
            #elif laser.y + laser_height <= star.y and laser.colliderect(star):
            #    print('slay')
            #try:
            #    stars.remove(star)
            #    del laser_hit
            #    print('laser and star delete')
            #except:
            #    pass
            #print('no dl')

            #elif laser_hit.colliderect(star):
            #    stars.remove(star)
            #    del laser_hit


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

        draw(player, elapsed_time, stars, health, highscore, lasers)

    if elapsed_time > highscore:
        highscore = elapsed_time
        with open('highscore.txt', 'w') as file:
            file.write(str(elapsed_time))

    pygame.quit()


if __name__ == "__main__":
     main()