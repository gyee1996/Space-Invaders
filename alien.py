import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    type1 = [pygame.image.load('images/type101.png'), pygame.image.load('images/type102.png'), pygame.image.load('images/pop.png')]
    type2 = [pygame.image.load('images/type201.png'), pygame.image.load('images/type202.png'), pygame.image.load('images/pop.png')]
    type3 = [pygame.image.load('images/type301.png'), pygame.image.load('images/type302.png'), pygame.image.load('images/pop.png')]

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.type = 0
        self.image = pygame.image.load('images/blank.png')
        self.count = 0
        self.end = 0
        self.fire = 0


        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.death = False
        self.x = float(self.rect.x)
        self.explosion = pygame.mixer.Sound('sounds/explosion.wav')


    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):

        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        if self.count >= 120:
            self.count = 0
        if self.death == False:

            if self.type == 1 and self.count < 60:
                self.image = self.type1[0]
            elif self.type == 1 and self.count >= 60:
                self.image = self.type1[1]
            elif self.type == 2 and self.count < 60:
                self.image = self.type2[0]
            elif self.type == 2 and self.count >= 60:
                self.image = self.type2[1]
            elif self.type == 3 and self.count < 60:
                self.image = self.type3[0]
            elif self.type == 3 and self.count >= 60:
                self.image = self.type3[1]
        else:
            self.dead()

        self.count += 1

    def dead(self):
        self.image = self.type1[2]

        if self.end >= 60:
            self.kill()
        else:
            self.end += 1
