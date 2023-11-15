import pygame

class Adversary(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health=100):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.image = pygame.image.load('assets/adversary/tornado.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.x += self.speed
        if self.x > 720 or self.x < 0:
            self.speed = -self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def lose_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.reset_health()

    def reset_health(self):
        self.health = 100
