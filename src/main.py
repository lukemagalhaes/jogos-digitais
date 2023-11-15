import pygame
import sys
from pygame.locals import *
from bullet import Bullet
from menu import Button
from player import Player
from adversary import Adversary

W, H = 720, 720
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Menu")

background = pygame.image.load('assets/background/level1.jpg')

def get_font(size):
    return pygame.font.Font("assets/menu/font.ttf", size)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(50, 530, bullets)
adversary = Adversary( 350, 415, 3)
adversary.image = pygame.transform.scale(adversary.image, (350, 350))
all_sprites.add(player, adversary)

shoot_delay = 3
last_shoot_time = pygame.time.get_ticks()

def play():
    global last_shoot_time
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w):
                player.isJumping = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - last_shoot_time > shoot_delay:
                    player.isShooting = True
                    new_bullet = Bullet(player.rect.x, player.rect.y)
                    mouse_pos = pygame.mouse.get_pos()
                    new_bullet.shoot(mouse_pos)
                    bullets.add(new_bullet)
                    last_shoot_time = current_time

        keys_pressed = pygame.key.get_pressed()

        clock.tick(FPS)
        screen.fill((30, 90, 120))
        screen.blit(background, (0, 0))

        player.move(keys_pressed)
        player.jump()

        adversary.move()

        for bullet in bullets:
            if not (0 <= bullet.rect.x <= W and 0 <= bullet.rect.y <= H):
                bullet.kill()
            elif pygame.sprite.collide_mask(bullet, adversary):
                bullet.kill()
                adversary.lose_health(1) 

        all_sprites.update()
        all_sprites.draw(screen)

        bullets.update()

        for bullet in bullets:
            if not (0 <= bullet.rect.x <= W and 0 <= bullet.rect.y <= H):
                bullet.kill()

        bullets.draw(screen)

        adversary.draw(screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f'Health: {adversary.health}', True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

def main_menu():
    global last_shoot_time
    while True:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(360, 100))

        play_button_image = pygame.image.load("assets/menu/Play Rect.png")
        quit_button_image = pygame.image.load("assets/menu/Quit Rect.png")

        new_button_size = (300, 75)
        play_button_image = pygame.transform.scale(play_button_image, new_button_size)
        quit_button_image = pygame.transform.scale(quit_button_image, new_button_size)

        PLAY_BUTTON = Button(image=play_button_image, pos=(360, 250),
                            text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White", action=play)
        QUIT_BUTTON = Button(image=quit_button_image, pos=(360, 350),
                            text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White", action=sys.exit)

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
                    PLAY_BUTTON.action()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    QUIT_BUTTON.action()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
