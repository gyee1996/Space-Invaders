import pygame
from pygame.sprite import Sprite

class Ebullet(Sprite):

    def __init__(self, ai_settings, screen, alien):
        super(Ebullet, self).__init__()
        self.screen = screen


        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom
        # Store the bullet's position as a decimal value

        self.y = float(self.rect.y)
        self.color = ai_settings.ebullet_color
        self.speed_factor = ai_settings.ebullet_speed_factor

    def update(self):
        # Update the decimal position of the bullet
        self.y -= self.speed_factor
        # Update Rect position
        self.rect.y = self.y

    def draw_ebullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)