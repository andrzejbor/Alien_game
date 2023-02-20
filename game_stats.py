class GameStats:
    """Monit statistic data in game"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        # Run game in active mode
        self.game_active = True

    def reset_stats(self):
        """Inicjalization statistic datat which can change during game"""
        self.ship_left = self.settings.ship_limit