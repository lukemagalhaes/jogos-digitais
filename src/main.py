import pygame
import sys
from pygame.locals import *
from bullet import Bullet
from menu import Button
from player import Player
from adversary import Adversary

W, H = 720, 720
FPS = 60
current_phase = 1  # Inicializa a fase atual

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Menu")

background = pygame.image.load('assets/background/level1.jpg')

def get_font(size):
    return pygame.font.Font("assets/menu/font.ttf", size)

players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
adversarys = pygame.sprite.Group()

player = Player(50, 530, bullets)
players.add(player)

adversary = Adversary(350, 415, 3, 1)
adversary.image = pygame.transform.scale(adversary.image, (350, 350))
adversarys.add(adversary)  # Adicione ao grupo 'adversarys'

shoot_delay = 3
last_shoot_time = pygame.time.get_ticks()

# Adicione uma variável global para a pontuação
score = 0

def play_next_phase():
    global current_phase, background, adversary

    # Adicione pontos ao passar para a próxima fase
    global score
    score += 10  # Ajuste conforme necessário

    if current_phase == 1:
        background = pygame.image.load('assets/background/level2.jpg')
        current_phase += 1
        adversarys.remove(adversary)
        player.fall(630)
        adversary = Adversary(350, 305, 10, 1)
        adversary.image = pygame.image.load('assets/adversary/furacao.png')
        adversary.image = pygame.transform.scale(adversary.image, (550, 550))
        adversarys.add(adversary)  # Adicione ao grupo 'adversarys'
    elif current_phase == 2:
        background = pygame.image.load('assets/background/level3.jpg')
        adversarys.remove(adversary)
        player.fall(650)
        adversary = Adversary(350, 305, 10, 1)
        adversary.image = pygame.image.load('assets/adversary/tufao.png')
        adversary.image = pygame.transform.scale(adversary.image, (160, 600))
        adversarys.add(adversary)  # Adicione ao grupo 'adversarys'

def play():
    global last_shoot_time, score
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
        if adversary.health <= 0:
            play_next_phase()

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

        if pygame.sprite.collide_mask(player, adversary):
            player.lose_health(1)

        players.update()
        players.draw(screen)

        bullets.update()

        for bullet in bullets:
            if not (0 <= bullet.rect.x <= W and 0 <= bullet.rect.y <= H):
                bullet.kill()

        bullets.draw(screen)

        adversarys.draw(screen)  # Desenhe a partir do grupo 'adversarys'

        font = pygame.font.Font(None, 36)
        text_hpAdversary = font.render(f'Health Adversary: {adversary.health}', True, (255, 255, 255))
        text_hpPlayer = font.render(f'Health Player: {player.health}', True, (255, 255, 255))
        text_score = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(text_hpAdversary, (10, 10))
        screen.blit(text_hpPlayer, (10, 50))
        screen.blit(text_score, (10, 90))

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
