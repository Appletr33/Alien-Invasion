class Settings():
    """Stores settings for the program"""

    def __init__(self):
        """Static settings"""
        # screen
        self.screen_width = 800
        self.screen_height = 600

        # Ship Settings
        self.ship_speed_factor = 2
        self.ship_limit = 3

        # bullet Settings
        self.bullet_speed_factor = 2
        self.bullet_allowed = 5

        # Alien settings
        self.alien_speed_factor = .75
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # Meteor settings
        self.meteor_speed = 2
        self.meteor_allowed = 2

        # Speedup of the game
        self.speedup_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """dynamic settings"""
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 2
        self.alien_speed_factor = .75
        self.meteor_speed = 2

        # 1 = right -1
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase the speed"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.meteor_speed *= self.speedup_scale
