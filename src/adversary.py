import pygame

class Adversary(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health=10):  # Defina um valor padrão para health
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.image = pygame.image.load('assets/adversary/furacao.png')
        self.rect = self.image.get_rect(center=(x, y))

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
            # Adicione aqui qualquer ação que você deseja realizar quando o adversário fica sem vida
            self.reset_health()  # Opcional: redefinir a vida para um valor inicial

    def reset_health(self):
        self.health = 10  # Defina o valor inicial de vida desejado
