# asteroid_shooter/game.py
import pygame
from models import Rock, Spaceship
from utils import load_sprite, print_text, print_sub_text, load_sound, print_score

bullets = []
rocks = []
high_score = 0


class Asteroids:
    """This class represents the game Space Rocks. It is responsible for handling the game loop, input,
    game logic, and drawing objects on the screen."""
    def __init__(self, mode=pygame.display.set_mode((800, 600))):
        # Initialize pygame and set the title
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.message = ""
        self.screen = mode
        self.background = load_sprite("space", False)
        self.ship = Spaceship((400, 300))
        self.explosion = load_sound("explosion")
        self.score = 0
        self.is_game_over = False

        global rocks
        rocks = [
            Rock.create_random(self.screen, self.ship.position)
            for _ in range(6)
        ]

    def main_loop(self):
        """This function handles the game loop."""
        while True:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        """This function handles the input from the user."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if self.is_game_over:
                    if event.key == pygame.K_SPACE:
                        global rocks, bullets
                        bullets = rocks = []
                        self.__init__()
                        return  # Restart the game
                if event.key == pygame.K_SPACE:
                    self.ship.shoot()

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            quit()

        if self.ship is None:
            return

        if is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_DOWN]:
            self.ship.decelerate()
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate()

    @property
    def game_objects(self):
        """This function returns the game objects."""
        global bullets, rocks
        stuff = [*bullets, *rocks]

        if self.ship:
            stuff.append(self.ship)

        return stuff

    def _game_logic(self):
        """This function handles the game logic."""
        global bullets, rocks

        for obj in self.game_objects:
            obj.move(self.screen)

        rect = self.screen.get_rect()
        for bullet in bullets[:]:
            if not rect.collidepoint(bullet.position):
                bullets.remove(bullet)

        for bullet in bullets[:]:
            for rock in rocks[:]:
                if rock.collides_with(bullet):
                    self.explosion.play()
                    rocks.remove(rock)
                    rock.split()
                    bullets.remove(bullet)
                    self._calculate_score()
                    break

        if self.ship:
            for rock in rocks[:]:
                if rock.collides_with(self.ship):
                    self.ship = None
                    self.message = "You lost!"
                    self.is_game_over = True
                    break

        if not rocks and self.ship:
            self.message = "You won!"
            self.is_game_over = True

    def _calculate_score(self):
        """This function calculates the score of the player."""
        self.score += 10
        global high_score
        if high_score < self.score:
            high_score = self.score

    def _get_score(self):
        """This function returns the score of the player."""
        return self.score

    def _draw(self):
        """This function handles the drawing of objects in the game."""
        self.screen.blit(self.background, (0, 0))

        for obj in self.game_objects:
            obj.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        if self.is_game_over:
            message = "Game Over! Press SPACE to restart or ESC to quit."
            print_sub_text(self.screen, message, self.subtitle_font)

        print_score(self.screen, self.subtitle_font, self.score, high_score)

        pygame.display.flip()
        self.clock.tick(30)



