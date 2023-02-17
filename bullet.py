import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class managing bullets shooting by ship"""

    def __init__(self, ai_game):
        """Creat bullet at actual ship position"""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Creat bullet at (0, 0) and define propre position for it
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Horizontal bullet position defined by float
        self.y = float(self.rect.y)

    def update(self):
        """Moving bullet on screen"""

        # Update bullet position
        self.y -= self.settings.bullet_speed

        # Update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Display bullet on screen"""

        pygame.draw.rect(self.screen, self.color, self.rect)
