import pygame, sys
from pygame.locals import *
import math
from random import randrange

class Player:
    def __init__(self, gamespace):
        self.x = 250
        self.y = 250
        self.radius = 25
        self.speed = 250
        self.dir = [0,0,0,0] #up, down, left, right
        self.color = pygame.Color(255,128,0)
        self.health = 3
        self.gs = gamespace
        self.moving = 0
        self.counter = 0

    def draw(self):
        pygame.draw.circle(self.gs.screen, self.color, (self.x,self.y), self.radius)
    def tick(self):
        if self.counter: 
            self.counter -= 1
        yes = -1*self.dir[0] + self.dir[1]
        xes = -1*self.dir[2] + self.dir[3]
        if yes and xes:
            self.x += xes * (1/60.0) * self.speed * (1/math.sqrt(2))
            self.y += yes * (1/60.0) * self.speed * (1/math.sqrt(2))
        elif yes:
            self.y += yes * (1/60.0) * self.speed
        elif xes:
            self.x += xes * (1/60.0) * self.speed
        if self.gs.toFire and not self.counter:
            self.counter = 5
            mx, my = pygame.mouse.get_pos()
            angle = math.degrees(math.atan2(mx-self.x,my-self.y))
            self.gs.bullettes.append(Bullet(self.x,self.y,angle,self.gs))
    def move(self, key):
        if (key == K_RIGHT):
            self.dir[3] = 1
        elif (key == K_UP):
            self.dir[0] = 1
        elif (key == K_DOWN):
            self.dir[1] = 1
        elif (key == K_LEFT):
            self.dir[2] = 1
    def stop(self, key):
        if (key == K_RIGHT):
            self.dir[3] = 0
        elif (key == K_UP):
            self.dir[0] = 0
        elif (key == K_DOWN):
            self.dir[1] = 0
        elif (key == K_LEFT):
            self.dir[2] = 0


class Enemy:
     def __init__(self, gamespace):
        self.x =  randrange(640)
        self.y = randrange(480)
        self.color = pygame.Color(125,125,125)
        self.radius = 15 + randrange(10)
        self.speed = 100 + randrange(200)
        self.health = 3
        self.gs = gamespace
     def tick(self):
        self.x += (1/60.0) * self.speed
     def draw(self):
        pygame.draw.circle(self.gs.screen, self.color, (self.x,self.y), self.radius)
        
class Chaser(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self,gamespace)
        self.color = pygame.Color(255,0,0)
        self.radius = 15
    def tick(self):
        self.x += (1/60.0) * self.speed * math.cos(math.atan2(self.gs.player.x-self.x,self.gs.player.y-self.y))
        self.y -= (1/60.0) * self.speed * math.sin(math.atan2(self.gs.player.x-self.x,self.gs.player.y-self.y))
class Sweeper(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self,gamespace)
        self.color = pygame.Color(0,0,255)
    def tick(self):
        self.y += (1/60.0) * self.speed
class Expander(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self,gamespace)
        self.color = pygame.Color(0,255,0)
    def tick(self):
        self.radius += 1
class Bullet:
    def __init__(self,x,y,dir,gamespace):
        self.gs = gamespace
        self.size = 5
        self.rect = pygame.Rect(x,y,self.size,self.size)
        self.xspeed = 500.0*math.sin(math.radians(dir))
        self.yspeed = 500.0*math.cos(math.radians(dir))
        self.color = pygame.Color(255,255,255)
    def tick(self):
        self.rect.x += self.xspeed/60.0
        self.rect.y += self.yspeed/60.0
    def draw(self):
        pygame.draw.circle(self.gs.screen, self.color, self.rect.center, self.size)

        
class GameSpace:
    def main(self):
        pygame.init()
        self.toFire = 0
        self.size = self.width, self.height = 640, 480
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.enemies = []
        self.enemies.append(Enemy(self))
        self.enemies.append(Chaser(self))
        self.enemies.append(Sweeper(self))
        self.enemies.append(Expander(self))
        self.bullettes = []
        while 1:
            self.screen.fill(self.black)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    self.player.move(event.key)
                if event.type == KEYUP:
                    self.player.stop(event.key)
                if event.type == MOUSEBUTTONDOWN:
                    self.toFire = 1
                if event.type == MOUSEBUTTONUP:
                    self.toFire = 0
            for bul in self.bullettes:
                bul.tick()
                bul.draw()
            for en in self.enemies:
                en.tick()
                en.draw()
            self.player.tick()
            self.player.draw()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
