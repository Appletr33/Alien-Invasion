class GameStats():
    """Track stats for Alien Invasion"""

    def __init__(self, ai_settings):
        """Init stats"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start the game in an inactive state
        self.game_active = False

    def reset_stats(self):
        """Init stats that change"""
        self.ships_left = self.ai_settings.ship_limit
