import pygame
import random
class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullets
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = ( 255, 255, 255)
        self.bullets_allowed = 1
        '''# Ebullets
        self.ebullet_speed_factor = 1
        self.ebullet_color = (255, 0, 0)'''

        # Alien Settings
        self.alien_speed_factor = 3
        self.fleet_drop_speed = 5
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1


        # How Quickly the game speeds up
        self.speedup_scale = 1.2
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # Sounds
        self.laser = pygame.mixer.Sound('sounds/laser2.wav')
        self.bg_music = pygame.mixer.Sound('sounds/loop.wav')
        self.explosion = pygame.mixer.Sound('sounds/explosion.wav')
        self.oscillation = pygame.mixer.Sound('sounds/oscilattion.wav')
        self.music_count = 0
        self.music_scale = 1.1
        self.max_count = 500


    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1.1
        self.fleet_direction = 1
        self.ufo_speed_factor = 0.8

        # Scoring
        self.alien_points = 50
        self.ufo_points = random.choice((250, 500, 1000))

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.max_count /= self.music_scale





