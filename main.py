import pygame as game
import os
import time
import random

game.font.init()
win = game.display.set_mode((750,740))
# load all of that images
green_ship = game.image.load(os.path.join("assets","pixel_ship_green_small.png"))
blue_ship = game.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
red_ship = game.image.load(os.path.join("assets","pixel_ship_red_small.png"))
player_ship = game.image.load(os.path.join("assets","pixel_ship_yellow.png"))
# bullets here:
green_laser = game.image.load(os.path.join("assets","pixel_laser_green.png"))
red_laser = game.image.load(os.path.join("assets","pixel_laser_red.png"))
blue_laser = game.image.load(os.path.join("assets","pixel_laser_blue.png"))
yellow_laser = game.image.load(os.path.join("assets","pixel_laser_yellow.png"))
# background image
background = game.image.load(os.path.join("assets","background-black.png"))
background = game.transform.scale(background,(750,740))

# importing all that images +





COOLDOWN = 30
# the main ship class :
class Ship :

    def __init__(self , x,y,health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.image = None
        self.laser = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self , window):
        win.blit(self.image,(self.x,self.y))
        for laser in self.lasers :
            laser.draw(win)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers :
            laser.move(vel)
            if laser.off_screen() :
                self.lasers.remove(laser)
            elif laser.collision(obj) :
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= COOLDOWN :
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter +=1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x +4 , self.y , self.laser)
            self.lasers.append(laser)
            self.cool_down_counter = 1

# player ship :
class Player(Ship):
    def __init__(self , x , y , health = 100):
        super().__init__(x,y,health)
        self.image = player_ship
        self.laser = yellow_laser
        self.mask = game.mask.from_surface(self.image)
        self.max_health = health

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers :
            laser.move(vel)
            if laser.off_screen() :
                self.lasers.remove(laser)
            else :
                for obj in objs :
                    if laser.collision(obj) :
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self , window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self , win):
        game.draw.rect(win , (255,0,0) , (self.x,self.y + self.image.get_height() + 10 , self.image.get_width() , 10))
        game.draw.rect(win , (0,255,0) , (self.x,self.y + self.image.get_height() + 10 , self.image.get_width()* (self.health/100) , 10))


# enemy ship :
color_map = {
        "red" : (red_ship,red_laser),
        "green" : (green_ship,green_laser),
        "blue" : (blue_ship,blue_laser)
    }
class Enemy(Ship):

    def __init__(self , x ,y , color , health = 100):
        super().__init__(x,y,health)
        self.image , self.laser = color_map[color]
        self.mask = game.mask.from_surface(self.image)

    def move(self,speed):
        self.y += speed
class Laser :
    def __init__(self, x ,y , image , ):
        self.x = x
        self.y = y
        self.image = image
        self.mask = game.mask.from_surface(self.image)

    def draw(self,win):
        win.blit(self.image,(self.x,self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self):
        return not(self.y <= 750 and self.y > 0)

    def collision(self,obj):
        return collide(obj,self)


def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask , (offset_x,offset_y)) != None




def main():

    # variables :
    run = True
    lost = False
    FPS = 60
    level = 0
    lives = 5
    lost_count = 0
    main_font = game.font.SysFont("comicsans" , 50 )
    lost_font = game.font.SysFont("comicsans", 70)
    clock = game.time.Clock()
    enemies = []
    wave_lenght = 0
    speed = 1
    ship = Player(300,650)





    # window generator
    def redraw_window():
        # background
        win.blit(background,(0,0))

        # creating texts
        lives_label = main_font.render(f" lives : {lives} " , 1 , (255,255,255))
        level_label = main_font.render(f" level : {level} " , 1 , (255,255,255))

        # attach texts
        win.blit(level_label,(10,10))
        win.blit(lives_label,(400,10))

        # draw the ship
        ship.draw(win)

        # draw enemies
        for enemy in enemies :
            enemy.draw(win)

        # lost status
        if lost :
            lost_label = lost_font.render("game over" , 1 , (255,255,255))
            win.blit(lost_label,(200,375))





        # apply all of that changes
        game.display.update()







    # main loop of the game

    while run:
        clock.tick(FPS)
        redraw_window()

        # losing
        if lives == 0 or ship.health <= 0 :
            lost = True
            lost_count += 1
        if lost :
            if lost_count > FPS * 3 :
                run = False
            else:
                continue


        # enemy and level generator
        if len(enemies) == 0 :
            level += 1
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(60 , 680) , random.randrange(-1000 , -100) , random.choice(["red","green","blue"]))
                enemies.append(enemy)


        # exiting the game
        for event in game.event.get() :
            if event.type == game.QUIT :
                run = False
                quit()

        # moving the ship
        keys = game.key.get_pressed()
        if keys[game.K_a] and ship.x > 5 : # left
            ship.x -= 5
        if keys[game.K_d] and ship.x < 670: # right
            ship.x += 5
        if keys[game.K_w] and ship.y > 5 : # up
            ship.y -= 5
        if keys[game.K_s] and ship.y < 660 : # down
            ship.y += 5
        if keys[game.K_SPACE] :
            ship.shoot()

        # moving enemies
        for enemy in enemies[:]:
            enemy.move(speed)
            enemy.move_lasers(4 , ship)

            if collide(enemy,ship) :
                ship.health -= 10
                enemies.remove(enemy)

            if enemy.y > 750 :
                lives -= 1
                enemies.remove(enemy)

            if random.randrange(0,240) == 1 :
                enemy.shoot()



        ship.move_lasers(-6 , enemies)


def main_menu():
    title_font = game.font.SysFont("comicsans" , 70)
    run = True
    while run :
        win.blit(background, (0, 0))
        title_labl = title_font.render("press the mouse to begin..." , 1 , (255,255,255))
        win.blit(title_labl, (70,375))
        game.display.update()
        for event in game.event.get():
            if event.type == game.QUIT :
                run = False
            if event.type == game.MOUSEBUTTONDOWN :
                main()

    game.quit()

main_menu()