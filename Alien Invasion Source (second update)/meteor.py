import pygame
import random
from pygame.sprite import Sprite


class Meteor(Sprite):

    def __init__(self, ai_settings, screen):
        super(Meteor, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the meteor image
        self.image = pygame.image.load('images/meteor.bmp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 71))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start the Meteor in a random position
        self.rect.x = random.randrange(0, 800)
        self.rect.y = -300

        # Store the position as a float
        self.y = float(self.rect.y)

    def update(self):
        """move down"""
        self.y += self.ai_settings.meteor_speed
        self.rect.y = self.y

        # Rid of extra meteors
        if self.rect.top > self.ai_settings.screen_height:
            self.kill()

    def draw_meteor(self):
        """Display the bullet"""
        self.screen.blit(self.image, self.rect)
