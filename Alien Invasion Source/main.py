import pygame

from settings import Settings
from alien import Alien
from ship import Ship
import game_functions as gf
from pygame.sprite import Group


def run_game():
  # int game and create a screen object
  pygame.init()
  ai_settings = Settings()
  screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
  bkgc = (230, 230, 230)
  bkg = pygame.image.load('images/bkg4.jpg').convert()
  bkg = pygame.transform.scale(bkg, (800, 600))
  pygame.display.set_caption("Alien Invasion")
  clock = pygame.time.Clock()
  # make the ship appear and group bullets and aliens
  ship = Ship(ai_settings, screen)
  bullets = Group()
  aliens = Group()

  # make an Alien
  alien = Alien(ai_settings, screen)
  gf.create_fleet(ai_settings, screen, ship, aliens)
  while True:
    # main loop
    clock.tick(60)
    gf.check_events(ai_settings, screen, ship, bullets)
    ship.update()
    gf.update_bullets(bullets)
    gf.update_aliens(ai_settings, aliens)
    gf.update_screen(ai_settings, bkgc, bkg, screen, ship, aliens, bullets)
    # make the most recently drawn screen visisble
    pygame.display.flip()



run_game()
