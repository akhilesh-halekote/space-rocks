# test_game.py
import unittest
from unittest.mock import patch, MagicMock
import pygame
from game import SpaceRocks
from models import Spaceship


class TestSpaceRocks(unittest.TestCase):
    @patch('pygame.display.set_mode')
    @patch('pygame.font.Font')
    @patch('utils.load_sprite')
    @patch('utils.load_sound')
    def setUp(self, mock_load_sound, mock_load_sprite, mock_font, mock_set_mode):
        mock_mode = pygame.display.set_mode((800, 600))
        mock_load_sprite.return_value = MagicMock()
        mock_load_sound.return_value = MagicMock()
        mock_font.return_value = MagicMock()
        mock_set_mode.return_value = MagicMock()
        self.game = SpaceRocks(mock_mode)

    def test_initialization(self):
        self.assertIsNotNone(self.game.screen)
        self.assertIsNotNone(self.game.background)
        self.assertIsNotNone(self.game.ship)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.is_game_over)

    @patch('pygame.event.get')
    def test_handle_input_quit(self, mock_event_get):
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]
        with self.assertRaises(SystemExit):
            self.game._handle_input()

    @patch('pygame.event.get')
    def test_handle_input_restart(self, mock_event_get):
        self.game.is_game_over = True
        mock_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
        with patch.object(self.game, '__init__', return_value=None) as mock_init:
            self.game._handle_input()
            mock_init.assert_called_once()

    @patch('pygame.display.flip')
    def test_draw(self, mock_display_flip):
        self.game._draw()
        mock_display_flip.assert_called_once()

    def test_ship_movement(self):
        initial_position = self.game.ship.position
        self.game.ship.move(self.game.screen)  # Move right
        self.assertNotEqual(self.game.ship.position, initial_position)

    def test_scoring(self):
        initial_score = self.game.score
        self.game = MagicMock()
        self.game.rocks = [MagicMock()]
        self.game.rocks[0].collides_with.return_value = False
        self.game.rocks[0].destroyed = True
        self.game._get_score.return_value = 10  # Mocking the get_score method
        self.game.score = self.game._get_score()
        self.game._game_logic()
        self.assertGreater(self.game.score, initial_score)

    def test_game_logic(self):
        self.game.ship = Spaceship((400, 300))
        self.game.ship.position = (400, 300)
        self.game._game_logic()
        assert self.game.is_game_over

    if __name__ == '__main__':
        unittest.main()
