import sys
import pygame
from bullet import Bullet
from alien import Alien
from meteor import Meteor
from time import sleep

pygame.mixer.init()
fire_sound = pygame.mixer.Sound("sounds/laser.wav")
explosion_sound = pygame.mixer.Sound("sounds/Explosion.wav")
ship_explosion_sound = pygame.mixer.Sound("sounds/ship_explosion.wav")


def check_events_down(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def create_meteor(ai_settings, screen, meteors):
    if len(meteors) < ai_settings.meteor_allowed:
        meteor = Meteor(ai_settings, screen)
        meteors.add(meteor)


def fire_bullet(ai_settings, screen, ship, bullets):
    # create a bullet and add it to the group
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        fire_sound.play()


def check_events_up(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, meteors):
    """Respond to input"""
    # keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_events_down(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_events_up(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, meteors, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, meteors, mouse_x, mouse_y):
    """Start the game when the player clicks the play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_active = True

        # Empty the groups
        aliens.empty()
        bullets.empty()
        meteors.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, bkgc, bkg, screen, stats, ship, aliens, bullets, meteors, play_button):
    # position the ship and bkg
    screen.fill(bkgc)
    screen.blit(bkg, (0, 0))
    ship.blitme()
    aliens.draw(screen)
    meteors.draw(screen)

    # draw the bullets behind the ship and aliens and the meteors
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the play button when the game is inactive
    if not stats.game_active:
        play_button.draw_button()


def update_bullets(ai_settings, screen, ship, aliens, bullets, meteors):
    """updated the current bullet pos and limit the number of bullets on screen"""
    bullets.update()
    # rid of extra bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_object_collisions(ai_settings, screen, ship, aliens, bullets, meteors)


def update_meteors(ai_settings, stats, screen, ship, aliens, bullets, meteors):
    """updated the current bullet pos and limit the number of bullets on screen"""
    meteors.update()

    # Detect ship-alien collisions
    if pygame.sprite.spritecollideany(ship, meteors):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, meteors)


def check_bullet_object_collisions(ai_settings, screen, ship, aliens, bullets, meteors):
    pygame.sprite.groupcollide(bullets, meteors, True, False)
    for bullet in pygame.sprite.groupcollide(bullets, aliens, True, True):
        explosion_sound.play()
    if len(aliens) == 0:
        # Remove active bullets, speed up the game and create a new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


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
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
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


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, meteors):
    """Update the position of each alien in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    ground_hit(ai_settings, stats, screen, ship, aliens, bullets, meteors)
    aliens.update()

    # Detect ship-alien collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, meteors)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, meteors):
    """Respond if the ship is hit by an alien"""
    if stats.ships_left > 0:
        # If a ship gets hit, lose a life
        stats.ships_left -= 1
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Play ship explosion sound
    ship_explosion_sound.play()

    # Empty the groups of sprites
    aliens.empty()
    bullets.empty()
    meteors.empty()
    # Create a new fleet of aliens and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pause
    sleep(0.5)


def ground_hit(ai_settings, stats, screen, ship, aliens, bullets, meteors):
    """Check if aliens reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, meteors)
            break

