import pygame
W, H = 720, 720

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.image.load('assets/bullet/bullet.png')
        self.image = pygame.transform.scale(self.image, (7, 7))
        self.direction = (0, 0)
        self.state = "ready"

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        if self.state == "fire":
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

            # Verificar se a bala está fora dos limites
            if self.rect.left > W or self.rect.right < 0 or self.rect.top > H or self.rect.bottom < 0:
                self.state = "ready"

    def shoot(self, mouse_pos):
        if self.state == "ready":
            self.state = "fire"
            self.rect.x = self.rect.x + 40
            self.rect.y = self.rect.y + 40
            dx = mouse_pos[0] - self.rect.x
            dy = mouse_pos[1] - self.rect.y
            distance = max(abs(dx), abs(dy))
            if distance != 0:
                self.direction = (dx / distance, dy / distance)
