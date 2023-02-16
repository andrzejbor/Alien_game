import sys
import pygame
from settings import Settings
from  ship import Ship


class AlienInvasion:
    """Main class"""

    def __init__(self):
        """ Game initialization"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien invasion")

        self.ship = Ship(self)

        self.bg_color = (self.settings.bg_color)

    def run_game(self):
        """Run main loop"""
        while True:
            """Wait for key or mouse click"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            """Refresh screen in every iteration"""
            self.screen.fill(self.bg_color)
            self.ship.blitme()

            """Display last refresh screen"""
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
