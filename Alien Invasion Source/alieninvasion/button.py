import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        """Initialize button"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the size and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (173, 216, 230)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Make the rect object value and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Prep the button msg once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Render msg and center it to the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw the button to the screen and then draw the msg on top
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)





