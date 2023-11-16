import pygame

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, max_health, is_player=True):
        super().__init__()
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        self.is_player = is_player
        self.border_color = (0, 0, 0)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.update_color()

    def update(self, current_health):
        self.current_health = current_health
        self.update_color()

    def update_color(self):
        health_percentage = max(0, min(1, self.current_health / self.max_health))
        fill_color = (int(255 * (1 - health_percentage)), int(255 * health_percentage), 0)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        inner_rect = pygame.Rect(0, 0, int(self.width * health_percentage), self.height)
        pygame.draw.rect(self.image, fill_color, inner_rect)
        pygame.draw.rect(self.image, self.border_color, self.image.get_rect(), 2)
