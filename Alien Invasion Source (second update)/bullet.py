import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Create a bullet at the ships current pos"""

    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/laser.bmp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the pos as a float
        self.y = float(self.rect.y)

        # store the speed from ai_settings
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """movement of the bullet"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Display the bullet"""
        self.screen.blit(self.image, self.rect)
