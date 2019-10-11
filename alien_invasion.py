import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from Button import Button
from highscore import Highscorelist
from ship import Ship
from alien import Alien
from ufo import UFO
import game_functions as gf
from pygame.locals import *

def run_game():

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # play button
    play_button = Button(ai_settings, screen, "PLAY")
    hs = Highscorelist(ai_settings, screen, "HIGHSCORES")
    # Create an instance to store game statistics
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen)
    bullets = Group()
    #ebullets = Group()
    aliens = Group()
    alien = Alien(ai_settings, screen)
    ufos = Group()
    ufo = UFO(ai_settings, screen)

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)


    while True:
            gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, hs)
            if stats.game_active:
                ship.update()
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, ufos)
                #gf.update_ebullets(ai_settings, screen, stats, sb, ship, aliens)
                gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
                gf.update_ufo(ai_settings, screen, stats, sb, ship, bullets, ufos)
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, hs, ufos)




run_game()