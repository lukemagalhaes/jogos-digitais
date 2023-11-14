import pygame
import sys
from pygame.locals import *

W, H = 500, 500
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Menu")

background = pygame.image.load('assets/Background.png')

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def play():
    original_background = pygame.image.load('assets/background4.jpg')
    new_background_size = (500, 500)
    background = pygame.transform.scale(original_background, new_background_size)
    
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

def main_menu():
    while True:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(250, 100))
        
        play_button_image = pygame.image.load("assets/Play Rect.png")
        quit_button_image = pygame.image.load("assets/Quit Rect.png")   

        new_button_size = (300, 75)
        play_button_image = pygame.transform.scale(play_button_image, new_button_size)
        quit_button_image = pygame.transform.scale(quit_button_image, new_button_size)

        PLAY_BUTTON = Button(image=play_button_image, pos=(250, 250), 
                            text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=quit_button_image, pos=(250, 350), 
                            text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()