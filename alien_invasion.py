import sys
import pygame


class AlienInvasion:
    """Main class"""

    def __init__(self):
        """ Game initialization"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien invasion")

        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Run main loop"""
        while True:
            """Wait for key or mouse click"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            """Refresh screen in every iteration"""
            self.screen.fill(self.bg_color)

            """Display last refresh screen"""
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
