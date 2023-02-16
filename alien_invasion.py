import sys
import pygame
from settings import Settings
from ship import Ship


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
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """Reaction for mouse and keyboard event"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Reaction on key down event"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True

    def _check_keyup_events(self, event):
        """Reaction on key up event"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Refresh object on screen and go to new screen"""
        # Refresh screen in every iteration
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        # Display last refresh screen
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
