import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import MagicMock, patch, call


class TestGameFlow(unittest.TestCase):
    
    @patch('pygame.init')
    @patch('pygame.font.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_icon')
    @patch('pygame.display.set_caption')
    @patch('pygame.display.set_mode')
    @patch('pygame.time.Clock')
    @patch('pygame.image.load')
    @patch('pygame.mixer.Sound')
    def setUp(self, mock_sound, mock_image_load, mock_clock, 
              mock_set_mode, mock_set_caption, mock_set_icon,
              mock_mixer_init, mock_font_init, mock_pygame_init):
        mock_image_load.return_value = MagicMock()
        mock_sound.return_value = MagicMock()
        
        with patch('main.Game.load_levels'):
            with patch('main.Game.load_highscores'):
                from main import Game
                self.Game = Game
                
                game = object.__new__(Game)
                game.levels = [{"name": "Level 1", "maxcoins": 10, "array": []}]
                game.highscores = [0]
                game.running = True
                self.game_instance = game
    
    def test_new_method_resets_all_states(self):
        game = self.game_instance
        
        game.background_music = MagicMock()
        
        game.lost = True
        game.quit_level = True
        game.current_column_number = 100
        game.current_shift = 500
        game.score = 50
        game.last_background_x_pos = 1000
        
        with patch('main.Player') as mock_player:
            mock_player.return_value = MagicMock()
            with patch('pygame.sprite.Group') as mock_group:
                mock_group.return_value = MagicMock()
                
                self.Game.new(game)
                
                self.assertFalse(game.lost)
                self.assertFalse(game.quit_level)
                self.assertEqual(game.current_column_number, 0)
                self.assertEqual(game.current_shift, 0)
                self.assertEqual(game.score, 0)
                self.assertEqual(game.last_background_x_pos, 100)
    
    def test_player_initialization_resets_state(self):
        with patch('settings.GRAVITY', 1.2):
            from segway_jump_sprites.player import Player
            
            mock_game = MagicMock()
            mock_game.character_left_walking_1_image = MagicMock()
            mock_game.character_left_walking_2_image = MagicMock()
            mock_game.character_left_walking_3_image = MagicMock()
            mock_game.character_jump_1_image = MagicMock()
            mock_game.character_jump_2_image = MagicMock()
            
            with patch('pygame.mask.from_surface', return_value=MagicMock()):
                with patch('pygame.transform.flip', return_value=MagicMock()):
                    player = Player(mock_game)
                    
                    self.assertEqual(player.jumpboost, 0)
                    self.assertEqual(player.jumpbooston, 0)
                    self.assertEqual(player.speeddrop, 0)
                    self.assertEqual(player.speeddropon, 0)
                    self.assertEqual(player.rect.x, 120)
                    self.assertEqual(player.rect.y, -120)
                    self.assertEqual(player.speed.x, 0)
                    self.assertEqual(player.speed.y, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
