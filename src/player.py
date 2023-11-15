import pygame
from bullet import Bullet  # Certifique-se de ajustar o nome do arquivo conforme necessário

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets):
        super().__init__()

        self.spritesheet = pygame.image.load('assets/player/Cowboy4_walk with gun_0.png')
        self.current_frame = 0
        self.animation_frames = 4
        self.frame_width = 50
        self.frame_height = 55
        self.isJumping = False
        self.jumpCount = 10
        self.direction = "right"

        self.shoot_images = [
            pygame.image.load(f'assets/player/Cowboy4_shoot_{i}.png') for i in range(4)
        ]
        self.shoot_index = 0
        self.isShooting = False

        self.jump_shoot_images = [
            pygame.image.load(f'assets/player/Cowboy4_jump shoot_{i}.png') for i in range(4)
        ]
        self.jump_shoot_index = 0
        self.is_jump_shooting = False

        self.jump_image = pygame.image.load(
            f'assets/player/Cowboy4_jump without gun_0.png'
        )

        self.image = self.spritesheet.subsurface(
            pygame.Rect(0, 0, self.frame_width, self.frame_height)
        )
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bullets = bullets

    def update(self):
        if self.is_jump_shooting:
            self.image = self.jump_shoot_images[self.jump_shoot_index]
            self.jump_shoot_index = (self.jump_shoot_index + 1) % 4
            if self.jump_shoot_index == 0:
                self.is_jump_shooting = False
        elif self.isShooting:
            if self.direction == "left":
                self.image = pygame.transform.flip(self.shoot_images[self.shoot_index], True, False)
            else:
                self.image = self.shoot_images[self.shoot_index]
            self.shoot_index = (self.shoot_index + 1) % 4
            if self.shoot_index == 0:
                self.isShooting = False
        elif self.isJumping:
            self.image = self.jump_image
        else:
            frame_x = self.current_frame * self.frame_width
            self.image = self.spritesheet.subsurface(
                pygame.Rect(frame_x, 0, self.frame_width, self.frame_height)
            )
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)

    def move(self, keys_pressed):
        if keys_pressed[pygame.K_RIGHT]:
            if self.rect.x + 5 < 720 - 35:
                self.rect.x += 5
                self.direction = "right"
        if keys_pressed[pygame.K_LEFT]:
            if self.rect.x - 0 > -5:
                self.rect.x -= 5
                self.direction = "left"

    def jump(self):
        if self.isJumping:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.rect.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 10

    def shoot(self, mouse_pos):
        self.isShooting = True
        self.shoot_index = 0
        new_bullet = Bullet(self.rect.x, self.rect.y)
        new_bullet.shoot(mouse_pos)
        self.bullets.add(new_bullet)
