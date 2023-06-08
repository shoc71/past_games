import pygame, sys
import random, time
from pygame.locals import *

pygame.init()

fps = pygame.time.Clock()

blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)

screen_width = 400
screen_height = 600
size = screen_width, screen_height = 400,600
speed = 5

screen_size = pygame.display.set_mode(size)
screen_size.fill(white)
pygame.display.set_icon(pygame.image.load("player11.png"))
pygame.display.set_caption("dis ia  game")

exit = False

class Enemy(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.default_image_size = (100,100)
        self.image = pygame.transform.scale(self.image, self.default_image_size)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,screen_width-40),0)

    def move(self):
        self.rect.move_ip(0,speed)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30,370), 0)

    def draw(self, surface):
        surface.blit (self.image, self.rect)

class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.default_image_size = (60,100)
        self.image = pygame.transform.scale(self.image, self.default_image_size)
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        '''if self.rect.left > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0,-5)
        if self.rect.right < screen_width:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)'''
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5,0)
        if self.rect.right < screen_width:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5,0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

p1 = Player()
e1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(e1)
all_sprites = pygame.sprite.Group()
all_sprites.add(p1)
all_sprites.add(p1)

while not exit:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    p1.update()
    e1.move()

    screen_size.fill(white)
    p1.draw(screen_size)
    e1.draw(screen_size)

    if pygame.sprite.spritecollideany(p1, enemies):
          screen_size.fill(red)
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()  

    pygame.display.update()
    fps.tick(60)