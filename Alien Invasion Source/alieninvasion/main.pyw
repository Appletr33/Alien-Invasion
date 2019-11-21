import pygame

from settings import Settings
from alien import Alien
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button

def run_game():
    # int game and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    bkgc = (230, 230, 230)
    bkg = pygame.image.load('images/bkg4.jpg').convert()
    icon = pygame.image.load('images/alien.bmp').convert_alpha()
    bkg = pygame.transform.scale(bkg, (800, 600))
    pygame.display.set_caption("Alien Invasion")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    # Make a play button
    play_button = Button(ai_settings, screen, "Play")

    # make the ship appear and group bullets, aliens and meteors
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    meteors = Group()

    # Create an instance to store in game stats
    stats = GameStats(ai_settings)

    # make an Alien
    alien = Alien(ai_settings, screen)
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        # main loop
        clock.tick(60)
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, meteors)
        gf.update_screen(ai_settings, bkgc, bkg, screen, stats, ship, aliens, bullets, meteors, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, meteors)
            gf.update_aliens(ai_settings, stats, screen,  ship, aliens, bullets, meteors)
            gf.update_meteors(ai_settings, stats, screen, ship, aliens, bullets, meteors)
            gf.create_meteor(ai_settings, screen, meteors)
        # make the most recently drawn screen visible
        pygame.display.flip()


run_game()
