import pygame, sys
from pygame.locals import *
import math
from random import randrange, random

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
        self.powerups = [0,0,0] #red, blue, green

    def draw(self):
        pygame.draw.circle(self.gs.screen, self.color, (int(self.x),int(self.y)), int(self.radius))
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
        if self.x -self.radius < 0:
            self.x = self.radius
        elif self.x + self.radius > self.gs.width:
            self.x = self.gs.width - self.radius
        if self.y - self.radius < 0:
            self.y = self.radius
        elif self.y + self.radius > self.gs.height:
            self.y = self.gs.height - self.radius
        if self.gs.toFire and not self.counter:
            self.counter = 15
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
        self.gs = gamespace
        self.visible = True
        self.radius = 15 + randrange(10)
        self.x = self.gs.player.x
        self.y = self.gs.player.y
        while (self.x >= (self.gs.player.x - 1.5*self.gs.player.radius) and self.x <= (self.gs.player.x + 3*self.gs.player.radius)):
            self.x = randrange(self.radius,self.gs.width-self.radius)
        while (self.y >= (self.gs.player.y - 1.5*self.gs.player.radius) and self.y <= (self.gs.player.y + 3*self.gs.player.radius)):
            self.y = randrange(self.radius,self.gs.height-self.radius)
        self.color = pygame.Color(125,125,125)
        
        self.speed = 100 + randrange(200)
        self.health = 3
        
    def collide(self):
        if math.sqrt(math.pow((self.x-self.gs.player.x),2) + math.pow((self.y - self.gs.player.y),2)) - self.radius - self.gs.player.radius <= 0:
            self.gs.player.health -= 1
            self.gs.enemies.remove(self)
            return
        if self.gs.player.health <=0:
            pygame.quit()
            sys.exit()
        for i in self.gs.bullettes:
            if math.sqrt(math.pow((self.x-i.rect.centerx),2) + math.pow((self.y - i.rect.centery),2)) - self.radius - i.radius <= 0:
                self.health-=1
                self.gs.bullettes.remove(i)
        if self.health <= 0:
            self.gs.enemies.remove(self)
            return
        for i in self.gs.enemies:
            if i == self or i.visible==False:
                continue
            while (math.sqrt(math.pow((self.x-i.x),2) + math.pow((self.y - i.y),2)) - self.radius - i.radius) <= 0:
                # print str(self.x) + ', ' + str(self.y)
                self.x -= .5*math.cos(math.atan2(self.y-i.y,i.x-self.x))
                self.y += .5*math.sin(math.atan2(self.y-i.y,i.x-self.x))
                i.x += .5*math.cos(math.atan2(self.y-i.y,i.x-self.x))
                i.y -= .5*math.sin(math.atan2(self.y-i.y,i.x-self.x))

    def draw(self):
        pygame.draw.circle(self.gs.screen, self.color, (int(self.x),int(self.y)), int(self.radius))
        
class Chaser(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self,gamespace)
        self.color = pygame.Color(255,0,0)
        self.radius = 15
        self.speed = 100 + randrange(100)
    def tick(self):
        self.x += (1/60.0) * self.speed * math.cos(math.atan2(self.y-self.gs.player.y,self.gs.player.x-self.x))
        self.y -= (1/60.0) * self.speed * math.sin(math.atan2(self.y-self.gs.player.y,self.gs.player.x-self.x))
        self.collide()

class Sweeper(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self,gamespace)
        self.color = pygame.Color(0,0,255)
        self.speed = 100 + randrange(100)
    def tick(self):
        self.x += (1/60.0) * self.speed * math.cos(math.atan2(self.y-self.gs.player.y,self.gs.player.x-self.x)+math.pi/4)
        self.y -= (1/60.0) * self.speed * math.sin(math.atan2(self.y-self.gs.player.y,self.gs.player.x-self.x)+math.pi/4)
        self.collide()

class Expander(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self,gamespace)
        self.color = pygame.Color(0,255,0)
    def tick(self):
        self.radius += 0.5
        self.collide()

class Bouncer(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self, gamespace)
        self.speed = 300 + randrange(100)
        self.color = pygame.Color(255,255,0)
        dir = random()*2*math.pi
        self.vx = math.cos(dir)*self.speed
        self.vy = math.sin(dir)*self.speed
    def tick(self):
        if self.x+self.radius >= self.gs.width or self.x-self.radius <= 0:
            self.vx *= -1
        if self.y+self.radius >= self.gs.height or self.y-self.radius <= 0:
            self.vy *= -1
        self.x += (1/60.0) * self.vx
        self.y += (1/60.0) * self.vy
        self.collide()
        
class Fader(Enemy):
    def __init__(self, gamespace):
        Enemy.__init__(self, gamespace)
        self.c = 255
        self.color = pygame.Color(0,self.c,self.c)
    
    def tick(self):
        if math.sqrt(math.pow((self.x-self.gs.player.x),2) + math.pow((self.y - self.gs.player.y),2)) - self.radius - self.gs.player.radius <= 300:
            self.visible = True
            self.x += (1/60.0) * self.speed * math.cos(math.atan2(self.y-self.gs.player.y,self.gs.player.x-self.x))
            self.y -= (1/60.0) * self.speed * math.sin(math.atan2(self.y-self.gs.player.y,self.gs.player.x-self.x))
            if self.c < 252:
                self.c += 4
                self.color = pygame.Color(0,self.c,self.c)
        else:
            if self.c > 3:
                self.c -= 4
                self.color = pygame.Color(0,self.c,self.c)
            else:
                self.visible = False
        if self.visible:
            self.collide()

class Bullet:
    def __init__(self,x,y,dir,gamespace):
        self.gs = gamespace
        self.radius = 7
        self.rect = pygame.Rect(x,y,self.radius,self.radius)
        self.xspeed = 500.0*math.sin(math.radians(dir))
        self.yspeed = 500.0*math.cos(math.radians(dir))
        if max(self.gs.player.powerups) != 0:
            self.color = pygame.Color(self.gs.player.powerups[0]*200/max(self.gs.player.powerups),self.gs.player.powerups[1]*200/max(self.gs.player.powerups),self.gs.player.powerups[2]*200/max(self.gs.player.powerups))
        else:
            self.color = pygame.Color(0,0,0)
    def tick(self):
        self.rect.x += self.xspeed/60.0
        self.rect.y += self.yspeed/60.0
    def draw(self):
        pygame.draw.circle(self.gs.screen, pygame.Color(255,255,255), self.rect.center, self.radius+1)
        pygame.draw.circle(self.gs.screen, self.color, self.rect.center, self.radius)

class Powerup:
    def __init__(self, gamespace):
        self.type = randrange(3)
        self.radius = 10
        self.gs = gamespace
        self.rect = pygame.Rect(randrange(self.gs.width-self.radius*2),randrange(self.gs.height-self.radius*2),self.radius*2,self.radius*2)
        self.color = pygame.Color((self.type==0)*255,(self.type==1)*255,(self.type==2)*255)
    def draw(self):
        pygame.draw.rect(self.gs.screen, self.color, self.rect)
    def tick(self):
        self.rect.x = self.rect.x
        self.collide()
    def collide(self):
        if math.sqrt(math.pow((self.rect.centerx-self.gs.player.x),2) + math.pow((self.rect.centery - self.gs.player.y),2)) - self.radius - self.gs.player.radius <= 0:
            self.gs.player.powerups[self.type] += 1
            self.gs.powerups.remove(self)
        
class GameSpace:
    def main(self):
        pygame.init()
        self.toFire = 0
        self.size = self.width, self.height = 1024, 768
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.enemies = []
        #self.enemies.append(Enemy(self))
        #self.enemies.append(Expander(self))
        #self.enemies.append(Chaser(self))
        #self.enemies.append(Sweeper(self))
        #self.enemies.append(Bouncer(self))
        self.enemies.append(Fader(self))
        self.bullettes = []
        self.spawns = 2
        self.powerups = []
        while 1:
            if len(self.enemies)==0:
                self.powerups.append(Powerup(self))
                self.spawns += 1
                for i in range(self.spawns):
                    x = randrange(5)
                    if x==0:
                        self.enemies.append(Expander(self))
                    elif x==1:
                        self.enemies.append(Chaser(self))
                    elif x==2:
                        self.enemies.append(Sweeper(self))
                    elif x==3:
                        self.enemies.append(Bouncer(self))
                    elif x==4:
                        self.enemies.append(Fader(self))
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
            for p in self.powerups:
                p.tick()
                p.draw()
            for bul in self.bullettes:
                bul.tick()
                bul.draw()
            for en in self.enemies:
                en.tick()
                if en.visible:
                	en.draw()
            self.player.tick()
            self.player.draw()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
