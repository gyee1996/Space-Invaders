import sys
from time import sleep
import pygame
import random
from bullet import Bullet
from alien import Alien
from ufo import UFO
#from ebullet import Ebullet


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def get_number_aliens_x(ai_settings, alien_width):
   available_space_x = ai_settings.screen_width - 2 * alien_width
   number_aliens_x = int(available_space_x / (2 * alien_width))
   return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - 3* alien_height  - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
def create_ufo(ai_settings, screen, stats, ufos):
    if random.randint(1, 8000) == 1 and len(ufos) == 0:
        ufo = UFO(ai_settings,screen)
        ufo.x = 0
        ufo.rect.x = ufo.x
        ufos.add(ufo)
        ai_settings.oscillation.play()


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)

    if row_number == 0:
        alien.type = 1
    elif row_number == 1 or row_number == 2:
        alien.type = 2
    elif row_number == 3 or row_number == 4:
        alien.type = 3
    alien_width = alien.rect.width
    alien.x = alien_width + alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 100 + alien.rect.height + 1 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # Create and alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
    '''for a in aliens:
        check_random_fire(ai_settings, stats, screen, a, bullets)'''
def update_ufo(ai_settings, screen, stats, sb, ship, bullets, ufos):
    create_ufo(ai_settings, screen, stats, ufos)
    ufos.update()

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_keydown_events(event,ai_settings,stats,  screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
         ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, stats, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, hs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings,stats, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            check_hs_button(ai_settings, screen, stats, sb, hs, ship, aliens, bullets, mouse_x, mouse_y)
            check_back_button(ai_settings,screen, stats, sb, hs, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_hs_button(ai_settings, screen, stats, sb, hs, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = hs.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.highscores = True
def check_back_button(ai_settings,screen, stats, sb, hs, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = sb.back_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.highscores = False

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, hs, ufos):
    screen.fill(ai_settings.bg_color)
    titlefont = pygame.font.SysFont(None, 96)
    titlescreen = titlefont.render('SPACE INVADERS', True, (255, 255, 255), ai_settings.bg_color)
    titlerect = titlescreen.get_rect()
    titlerect.right = 900
    titlerect.top = 20

    for bullet in bullets.sprites():

        bullet.draw_bullet()

    '''for ebullet in ebullets.sprites():
        ebullet.draw_ebullet()'''



    if stats.game_active:
        ship.blitme()
        aliens.draw(screen)
        ufos.draw(screen)
        # Draw the score info
        sb.show_score()
        play_music(ai_settings, aliens)




    # draw the play button if the game is inactive
    if not stats.game_active and not stats.highscores:
        play_button.draw_button()
        screen.blit(titlescreen, titlerect)
        hs.draw_button()

    if not stats.game_active and stats.highscores:
        sb.load_highscores()

    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, ufos):
    # update bullet positions
    bullets.update()
    # remove bullet if it hits an alien

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_bullet_ufo_collisions(ai_settings, screen, stats, sb, ship, ufos, bullets)
'''
def update_ebullets(ai_settings, screen, stats, sb, ship, aliens, ebullets):
    ebullets.update()

    for ebullet in ebullets.copy():
        if ebullet.rect.top >= ai_settings.screen_height:
            ebullets.remove(ebullet)
    check_ebullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens,ebullets)
'''

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    for bullet in bullets:
        alien = pygame.sprite.spritecollide(bullet, aliens, False)
        for a in alien:
            a.death = True
            bullet.kill()
            ai_settings.explosion.play()


            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_bullet_ufo_collisions(ai_settings,screen, stats, sb, ship, ufos, bullets):
    for bullet in bullets:
        ufo = pygame.sprite.spritecollide(bullet, ufos, False)
        for u in ufo:
            u.death = True
            bullet.kill()
            ai_settings.explosion.play()
            ai_settings.ufo_points = random.choice((250, 500, 1000))
            stats.score += ai_settings.ufo_points * stats.level
            sb.prep_score()
        check_high_score(stats, sb)

'''def check_ebullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, ebullets):
    for ebullet in ebullets:
        sh = pygame.sprite.spritecollide(ship, ebullets, False)
        for s in sh:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)'''



'''def check_random_fire(ai_settings, stats, screen, alien, ebullets):
    alien.fire = random.randint(1, 10000000)
    if alien.fire >= 9999900:
        print(alien.fire)
        enemy_fire(ai_settings,stats, screen,alien, ebullets)
        alien.fire = 0'''

def fire_bullet(ai_settings,stats, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed and stats.game_active == True:
        new_bullet = Bullet(ai_settings, screen, ship)
        ai_settings.laser.play()
        bullets.add(new_bullet)



'''def enemy_fire(ai_settings, stats, screen, alien, ebullets):
    new_ebullet = Ebullet(ai_settings, screen, alien)
    ai_settings.laser.play()
    ebullets.add(new_ebullet)'''

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.high_score
        sb.prep_high_score()


def play_music(ai_settings, aliens):
    if ai_settings.music_count >= ai_settings.max_count:
        ai_settings.bg_music.play()
        ai_settings.music_count = 0
    ai_settings.music_count += 1