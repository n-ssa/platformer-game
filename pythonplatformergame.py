import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init()
vec = pygame.math.Vector2 #2d

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('game')

class Player(pygame.sprite.Sprite): #makes it easy to duplicate and access objects
    def __init__(self):
        super().__init__()
        #self.image = pygame.image.load('character.png')
        self.surf = pygame.Surface((30, 30)) #surface object with fixed size
        self.surf.fill((255,255,0)) #gives color(RGB)
        self.rect = self.surf.get_rect() #create rect object from surface

        self.pos = vec((10, 360)) #vec- used to create variables with two dimensions(velocity and acceleeration are vector quantities)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
      
        self.jumping = False 
        self.score = 0  #attribute score, keeps track of score, intialised from 0

    def move(self): #move function created
        self.acc = vec(0,0.5)  #resets value of acceleration to 0

        pressed_keys = pygame.key.get_pressed() #checks for pressed keys
        
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC #if left key is pressed it'll update acceleration with a negative value
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC #if right key is pressed it'll update acceleration with a positive value
            
        self.acc.x += self.vel.x * FRIC #FRIC decreases the value of velocity
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #equation of motion

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0: #two if statements allows screen warping (go through left, come out of right)
            self.pos.x = WIDTH
    
        self.rect.midbottom = self.pos #updates the rect() object of player with new position that it gained after being moved

    def jump(self): #determins if player is jumping
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True 
            self.vel.y = -15
        
    def cancel_jump(self): #purpose is to decrease player's velocity
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
    
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:    
                        hits[0].point = False    #point attribute created and gives points depending on if player landed or not 
                        self.score += 1          #check point attribute of platform landed on
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False


class platform(pygame.sprite.Sprite): #makes it easy to duplicate and access objects
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12)) #surface objects with fixed size
        self.surf.fill((0,255,0)) #gives color
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10), random.randint(0, HEIGHT-30))) #create rect object from surface
    
        self.moving = True
        self.point = True    #

    def move(self):
        pass

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue 
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True 
        C = False

def plat_gen():
    while len(platforms) < 6:  #code runs only when theres less than 7 platforms on screen
        width = random.randrange(50,100)  #assigns random width to new platforms
        p = platform()
        C = True
       
        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
            C = check(p, platforms)

        platforms.add(p)
        all_sprites.add(p)  #creates and places platform above the visable part of the screen, position randomly generated using the random library

PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

all_sprites = pygame.sprite.Group() 
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

PT1.moving = False
PT1.point = False   #

for x in range(random.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump() 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()
        if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                sys.exit()

    if P1.rect.top <= HEIGHT / 3:  #checks to see the position of player with respect to screen
        P1.pos.y += abs(P1.vel.y)   #everytime players position reaches 'HEIGHT / 3' this statement is executed
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)  #screen no longer dynamic object, player position must keep being updated, 'abs()' used to remove negative sign from velocity
            if plat.rect.top >= HEIGHT:
                plat.kill()               #player position updated, same must be done for every sprite on screeen, iterate through all platforms in latform group and update their position. destroys any platforms that go off screen from bottom
    


    plat_gen()      
    displaysurface.fill((0,0,0)) #background color
    f = pygame.font.SysFont("Verdana", 20)     #
    g = f.render(str(P1.score), True, (123,255,0))    #
    displaysurface.blit(g, (WIDTH/2, 10))     #
   
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect) #
        entity.move()
    
    pygame.display.update()
    FramePerSec.tick(FPS)


    #prcacticing gitbash
    #helphelphelphelphelp