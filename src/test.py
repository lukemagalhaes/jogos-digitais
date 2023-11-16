import unittest
from unittest.mock import Mock, patch
import pygame
from player import Player

class TestPlayer(unittest.TestCase):

    def test_inicializacao_player(self):
        bullets_mock = Mock()
        player = Player(50, 100, bullets_mock)
        self.assertEqual(player.rect.x, 50)
        self.assertEqual(player.rect.y, 100)
        self.assertEqual(player.health, 100)
        self.assertFalse(player.isJumping)
        self.assertEqual(player.jumpCount, 10)
        self.assertEqual(player.direction, "right")
        self.assertEqual(player.shoot_index, 0)
        self.assertFalse(player.isShooting)
        self.assertEqual(player.jump_shoot_index, 0)
        self.assertFalse(player.is_jump_shooting)

    def test_perda_de_vida(self):
        bullets_mock = Mock()
        player = Player(50, 100, bullets_mock)
        player.lose_health(20)
        self.assertEqual(player.health, 80)

    def test_movimentacao_player_direita(self):
        bullets_mock = Mock()
        player = Player(50, 100, bullets_mock)
        player.move({pygame.K_RIGHT: True})
        self.assertEqual(player.rect.x, 55) 

    def test_movimentacao_player_esquerda(self):
        bullets_mock = Mock()
        player = Player(50, 100, bullets_mock)
        player.move({pygame.K_LEFT: True})
        self.assertEqual(player.rect.x, 45)  # Ajuste conforme a lógica real de movimentação

    def test_pulo_do_player(self):
        bullets_mock = Mock()
        player = Player(50, 100, bullets_mock)
        player.jump()
        self.assertTrue(player.isJumping) 

    def test_shoot_do_player(self):
        bullets_mock = Mock()
        player = Player(50, 100, bullets_mock)
        player.shoot((100, 150)) 
        self.assertTrue(player.isShooting)
        self.assertEqual(player.shoot_index, 0)

    def test_reset_do_player(self):
        bullets_mock = Mock()
        player = Player(50, 100, bullets_mock)
        player.isJumping = True
        player.jumpCount = 5
        player.direction = "left"
        player.health = 50
        player.isShooting = True
        player.shoot_index = 2
        player.is_jump_shooting = True
        player.jump_shoot_index = 3

        player.reset()

        self.assertFalse(player.isJumping)
        self.assertEqual(player.jumpCount, 10)
        self.assertEqual(player.direction, "right")
        self.assertEqual(player.health, 100)
        self.assertFalse(player.isShooting)
        self.assertEqual(player.shoot_index, 0)
        self.assertFalse(player.is_jump_shooting)
        self.assertEqual(player.jump_shoot_index, 0)

if __name__ == '__main__':
    unittest.main()
