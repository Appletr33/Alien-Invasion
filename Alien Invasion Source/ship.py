import pygame

class Ship():

  def __init__(self, ai_settings, screen):
    self.screen = screen

    #load the ship image
    self.image = pygame.image.load('images/ship.bmp').convert_alpha()
    self.image = pygame.transform.scale(self.image, (36, 50))
    self.rect = self.image.get_rect()
    self.screen_rect = screen.get_rect()
    self.ai_settings = ai_settings

    #start the ship in the bottom of the screen
    self.rect.centerx = self.screen_rect.centerx
    self.rect.bottom =self.screen_rect.bottom

    #store the ship's cetner as a float
    self.center = float(self.rect.centerx)

    #flags for movement
    self.moving_right = False
    self.moving_left = False

  def update(self):
    """Update the position of the ship base on the movement flags"""
    if self.moving_right and self.rect.right < self.screen_rect.right:
      self.center += self.ai_settings.ship_speed_factor
    if self.moving_left and self.rect.left > 0:
      self.center -= self.ai_settings.ship_speed_factor

    #update the rect from self.center 
    self.rect.centerx = self.center

  def blitme(self):
    """draw the ship at its current pos"""
    self.screen.blit(self.image, self.rect)