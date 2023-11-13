import pygame
import sys
from pygame.locals import *

W, H = 500, 500
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))

background = pygame.image.load('assets/background5.jpg')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spritesheet = pygame.image.load('assets/player/Cowboy4_walk with gun_0.png')
        self.current_frame = 0
        self.animation_frames = 4
        self.frame_width = 50
        self.frame_height = 55
        self.isJump = False
        self.jumpCount = 10
        self.direction = "right"  # Inicialmente o jogador está voltado para a direita

        self.shoot_images = [pygame.image.load(f'assets/player/Cowboy4_shoot_{i}.png') for i in range(4)]
        self.shoot_index = 0
        self.shoot_image = None
        self.is_shooting = False

        self.jump_shoot_images = [pygame.image.load(f'assets/player/Cowboy4_jump shoot_{i}.png') for i in range(4)]
        self.jump_shoot_index = 0
        self.jump_shoot_image = None
        self.is_jump_shooting = False

        self.jump_image = pygame.image.load(f'assets/player/Cowboy4_jump without gun_0.png')

    def draw(self):
        if self.is_jump_shooting:
            self.jump_shoot_image = self.jump_shoot_images[self.jump_shoot_index]
            screen.blit(self.jump_shoot_image, (self.x, self.y))
            self.jump_shoot_index = (self.jump_shoot_index + 1) % 4
            if self.jump_shoot_index == 0:
                self.is_jump_shooting = False
        elif self.is_shooting:
            self.shoot_image = self.shoot_images[self.shoot_index]
            screen.blit(self.shoot_image, (self.x, self.y))
            self.shoot_index = (self.shoot_index + 1) % 4
            if self.shoot_index == 0:
                self.is_shooting = False
        elif self.isJump:
            screen.blit(self.jump_image, (self.x, self.y))
        else:
            frame_x = self.current_frame * self.frame_width
            player_image = self.spritesheet.subsurface(pygame.Rect(frame_x, 0, self.frame_width, self.frame_height))
            if self.direction == "right":
                screen.blit(player_image, (self.x, self.y))
            else:
                player_image = pygame.transform.flip(player_image, True, False)
                screen.blit(player_image, (self.x, self.y))

    def move(self):
        if pressed_keys[K_RIGHT]:
            if self.x + 5 < W - 35:
                self.x += 5
                self.direction = "right"
        if pressed_keys[K_LEFT]:
            if self.x - 5 > -5:
                self.x -= 5
                self.direction = "left"

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount**2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

    def shoot(self):
        self.is_shooting = True
        bullet_x = self.x  # Mantém a posição atual do jogador para o tiro
        if self.direction == "left":
            bullet_x -= 20  # Ajusta a posição do tiro para a esquerda
        new_bullet = Bullet(bullet_x, self.y)
        bullets.append(new_bullet)
        
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.image.load('assets/bullet.png')
        self.image = pygame.transform.scale(self.image, (7, 7))
        self.direction = (0, 0)
        self.state = "ready"

    def draw(self):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))

    def shoot(self, mouse_pos):
        if self.state == "ready":
            self.state = "fire"
            self.x = player.x + 40
            self.y = player.y + 40
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            distance = max(abs(dx), abs(dy))
            if distance != 0:
                self.direction = (dx / distance, dy / distance)

    def move(self):
        if self.state == "fire":
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
            if not (0 <= self.x <= W and 0 <= self.y <= H):
                self.state = "ready"

player = Player(50, 350)
bullets = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.isJump = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shoot()
            mouse_pos = pygame.mouse.get_pos()
            new_bullet = Bullet(player.x, player.y)
            new_bullet.shoot(mouse_pos)
            bullets.append(new_bullet)

    clock.tick(FPS)
    pressed_keys = pygame.key.get_pressed()
    screen.fill((30, 90, 120))
    screen.blit(background, (0, 0))
    player.move()
    player.draw()
    player.jump()

    for bullet in bullets:
        bullet.move()
        bullet.draw()

    pygame.display.update()
