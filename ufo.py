import pygame
import random
from pygame.sprite import Sprite

class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.death = False
        self.end = 0
        self.direction = 0
        self.font = pygame.font.SysFont(None, 36)
        self.score_image = self.font.render(str(self.ai_settings.ufo_points), True, (0, 255, 0), self.ai_settings.bg_color)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.left > 1200:
            self.kill()
        elif self.rect.right < 0:
            self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.ufo_speed_factor * 1)
        self.rect.x = self.x
        if self.death == True:
            self.dead()
        self.check_edges()


    def dead(self):
        self.image = self.score_image

        if self.end >= 60:
            self.kill()
        else:
            self.end += 1