import pygame
import sys
from pygame.locals import *
from bullet import Bullet
from menu import Button
from player import Player

W, H = 720, 720
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Menu")

background = pygame.image.load('assets/background/background4.jpg')

def get_font(size): # Retorna a fonte Press-Start-2P no tamanho desejado
    return pygame.font.Font("assets/menu/font.ttf", size)

# Create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(50, 530, bullets)
all_sprites.add(player)

shoot_delay = 300  # 300 milissegundos
last_shoot_time = pygame.time.get_ticks()

def play():
    global last_shoot_time  # Declare a variável como global
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
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

        # Move e pula o jogador
        player.move(keys_pressed)
        player.jump()

        # Update all sprites
        all_sprites.update()

        # Draw all sprites
        all_sprites.draw(screen)

        # Update and draw bullets
        bullets.update()

        # Remove bullets marked as "ready"
        for bullet in bullets:
            if not (0 <= bullet.rect.x <= W and 0 <= bullet.rect.y <= H):
                bullet.kill()

        # Draw bullets
        bullets.draw(screen)

        pygame.display.flip()

# Função do menu
def main_menu():
    global last_shoot_time  # Declare a variável como global
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

# Loop do menu
if __name__ == "__main__":
    main_menu()
