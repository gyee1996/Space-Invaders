import pygame.font
from pygame.sprite import Group
from ship import Ship
import pickle
from operator import itemgetter

class Scoreboard():

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.highscores = []
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_back()
        self.index = 0


    def prep_score(self):
        score_str = str(self.stats.score)
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}" .format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}" .format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 780
            self.ships.add(ship)
    '''
    def load_highscores(self):
        
        with open ('textfiles/highscores.txt', 'r') as h:
            highscores = pickle.load(h)
            for hs in highscores:
                hs.image = self.font.render(hs, True, self.text_color)
                hs.rect = hs.image.get_rect()
                hs.rect.center = (600, 100 * self.index)
                self.screen.blit(hs.image, hs.rect)
                self.index += 1
            self.index = 0


    def save_highscores(self):
        highscores.append(self.score)
        highscores = sorted(highscores, key=itemgetter(1), reverse=True)[:10]
        with open('textfiles/highscores.txt', 'w') as h:
            pickle.dump(highscores, h)
    '''

    def load_highscores(self):
        self.screen.blit(self.back_image, self.back_rect)

    def prep_back(self):
        self.back_image = self.font.render('>BACK<', True, self.text_color)
        self.back_rect = self.back_image.get_rect()
        self.back_rect.center = (600, 700)