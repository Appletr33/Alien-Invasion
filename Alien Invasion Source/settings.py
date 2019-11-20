import pygame

class Settings():
  """Stores settings for the program"""

  def __init__(self):
    #screen
    self.screen_width = 800
    self.screen_height = 600

    #Ship Settings
    self.ship_speed_factor = 2

    #bullet Settings
    self.bullet_speed_factor = 2
    self.bullet_allowed = 5

    #Alien settings
    self.alien_speed_factor = .5
    self.fleet_drop_speed = 10
    self.fleet_direction = 1