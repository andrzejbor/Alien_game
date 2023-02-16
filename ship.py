import pygame


class Ship:
    """Class for managing ship"""

    def __init__(self, ai_game):
        """Initialization ship and default position"""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings

        # Load ship image and rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # New ship appear on screen bottom
        self.rect.midbottom = self.screen_rect.midbottom

        # Use float number to storage horizontal ship position
        self.x = float(self.rect.x)

        # Option showing ship moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update ship position depending on key events"""

        # Update ship x position
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed

        # Update rect object depending on x value
        self.rect.x = self.x

    def blitme(self):
        """Display ship in actual position"""
        self.screen.blit(self.image, self.rect)
