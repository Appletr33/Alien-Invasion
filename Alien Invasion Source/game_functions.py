import sys

import pygame
from bullet import Bullet
from alien import Alien
pygame.mixer.init()
fire_sound = pygame.mixer.Sound("sounds/laser.wav")

def check_events_down(event, ai_settings, screen, ship, bullets):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = True
  elif event.key == pygame.K_LEFT:
    ship.moving_left = True
  elif event.key == pygame.K_SPACE:
    fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
#create a bullet and add it to the group
    if len(bullets) < ai_settings.bullet_allowed:
      new_bullet = Bullet(ai_settings, screen, ship)
      bullets.add(new_bullet)
      pygame.mixer.Sound.play(fire_sound)
def check_events_up(event, ship):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = False
  elif event.key == pygame.K_LEFT:
    ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
  """Respond to input"""
  #keyboard and mouse events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      check_events_down(event, ai_settings, screen, ship, bullets)
    elif event.type == pygame.KEYUP:
      check_events_up(event, ship)


def update_screen(ai_settings, bkgc, bkg, screen, ship, aliens, bullets):
  #position the ship and bkg
  screen.fill(bkgc)
  screen.blit(bkg, (0, 0))
  ship.blitme()
  aliens.draw(screen)

  #draw the bullets behind the ship and aliens
  for bullet in bullets.sprites():
    bullet.draw_bullet()


def update_bullets(bullets):
  """updated the current bullet pos and limit the number of bullets on screen"""
  bullets.update()
  #rid of extra bullets
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)


def get_number_aliens_x(ai_settings, alien_width):
  """calculate the number of aliens in a row"""
  available_space_x = ai_settings.screen_width - 1 * alien_width
  number_aliens_x = int(available_space_x / (2 * alien_width))
  return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
  """Determine the number of rows of aliens that can fit screen"""
  available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
  number_rows = int(available_space_y / (2 * alien_height))
  return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
  alien = Alien(ai_settings, screen)
  alien_width = alien.rect.width
  alien.x = alien_width + 2 * alien_width * alien_number
  alien.rect.x = alien.x
  alien.rect.y = alien.rect.height + 2 * alien.rect.height *row_number
  aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
  """Create a fleet of aliens"""
  # find the number of aliens in a row
  # Spacing between aleins is equal to their width
  alien = Alien(ai_settings, screen)
  number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
  number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

  # Create the number of aliens in a Row
  for row_number in range(number_rows):
    for alien_number in range(number_aliens_x):
      create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
  """check if an alien has reached the edge"""
  for alien in aliens.sprites():
    if alien.check_edges():
      change_fleet_direction(ai_settings, aliens)
      break


def change_fleet_direction(ai_settings, aliens):
  """move the fleet down and change the movement direction"""
  for alien in aliens.sprites():
    alien.rect.y += ai_settings.fleet_drop_speed
  ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens):
  """Update the position of each alien in the fleet"""
  check_fleet_edges(ai_settings, aliens)
  aliens.update()
