import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Main class"""

    def __init__(self):
        """ Game initialization"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien invasion")

        # Create object that will storage game data
        # Create object to storage score information
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Create button "Play"
        self.play_button = Button(self, "Play")

        self.bg_color = self.settings.bg_color

    def run_game(self):
        """Run main loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._check_bullet_alien_collisions()
                self._update_alien()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos
                                        )

    def _check_keydown_events(self, event):
        """Reaction on key down event"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Reaction on key up event"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start new game after click play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game stats
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Remove aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and put ship in center
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create new bullet and add it to group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_bullet_alien_collisions(self):
        """Update bullets position and remove outside screen bullets"""
        # Update bullets position
        self.bullets.update()

        # Check if any bullet hit alien, if yes remove bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # Update score points
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Remove outside screen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        if not self.aliens:
            # Remove bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increment level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create alien fleet"""
        # Create alien and max alien number in row. Distance between alien is alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Calculation how many row can fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create full alien fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create alien and put it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

        self.aliens.add(alien)

    def _update_alien(self):
        """CHeck if fleet reach screen edge, next update all aliens position"""
        self._check_fleet_edges()
        self.aliens.update()

        # Check collision between alien and ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if alien reach bottom
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Fleet reaction when alien reach screen edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Move all fleet down and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Reaction after alien hit ship"""
        if self.stats.ship_left > 0:
            # Decreasing value in ship_left
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Remove aliens and bullets content
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and move ship to middle
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any alien reach bottom of screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom:
                # React in the same way as in ship hit
                self._ship_hit()
                break

    def _update_screen(self):
        """Refresh object on screen and go to new screen"""
        # Refresh screen in every iteration
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw aliens
        self.aliens.draw(self.screen)

        # Display score
        self.sb.show_score()

        # Draw play button when game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Display last refresh screen
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
