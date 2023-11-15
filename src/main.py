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

background = pygame.image.load('assets/background/level1.jpg')

def get_font(size): # Retorna a fonte Press-Start-2P no tamanho desejado
    return pygame.font.Font("assets/menu/font.ttf", size)

# Create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(50, 530, bullets)
adversary = Adversary(W // 2 + 300, H // 2 + 130, 3)
adversary.image = pygame.transform.scale(adversary.image, (200, 350))
all_sprites.add(player, adversary)

shoot_delay = 300
last_shoot_time = pygame.time.get_ticks()

paused = False
pause_menu_buttons = []
sound_enabled = True

def play():
    global last_shoot_time, paused, pause_menu_buttons  # Declare a variável como global
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    player.isJumping = True
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        create_pause_menu_buttons()
                    else:
                        pause_menu_buttons = []

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - last_shoot_time > shoot_delay:
                    player.isShooting = True
                    new_bullet = Bullet(player.rect.x, player.rect.y)
                    mouse_pos = pygame.mouse.get_pos()
                    new_bullet.shoot(mouse_pos)
                    bullets.add(new_bullet)
                    last_shoot_time = current_time

                    # keys_pressed = pygame.key.get_pressed()

        if paused:
            show_pause_menu()
        else:
            keys_pressed = pygame.key.get_pressed()

            clock.tick(FPS)
            screen.fill((30, 90, 120))
            screen.blit(background, (0, 0))

            # Move e pula o jogador
            player.move(keys_pressed)
            player.jump()

        # Atualize a posição do adversário
        adversary.move()

        # Dentro do loop play()
        for bullet in bullets:
            if not (0 <= bullet.rect.x <= W and 0 <= bullet.rect.y <= H):
                bullet.kill()
            elif pygame.sprite.collide_rect(adversary, bullet):
                bullet.kill()
                adversary.lose_health(10)  # 10 é um exemplo, ajuste conforme necessário

        all_sprites.update()
        all_sprites.draw(screen)

            # Update and draw bullets
            bullets.update()

            # Remove bullets marked as "ready"
            for bullet in bullets:
                if not (0 <= bullet.rect.x <= W and 0 <= bullet.rect.y <= H):
                    bullet.kill()

            # Draw bullets
            bullets.draw(screen)

        # Desenhe o adversário
        adversary.draw(screen)

        # Exibir a vida do adversário na tela
        font = pygame.font.Font(None, 36)
        text = font.render(f'Health: {adversary.health}', True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

def toggle_sound():
    global sound_enabled
    if sound_enabled:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    sound_enabled = not sound_enabled

def resume_game():
    global paused
    paused = False

def create_pause_menu_buttons():
    global pause_menu_buttons

    sound_button_image = pygame.image.load("assets/menu/Play Rect.png")
    instructions_button_image = pygame.image.load("assets/menu/Play Rect.png")
    resume_button_image = pygame.image.load("assets/menu/Play Rect.png")

    new_button_size = (300, 75)
    instruction_button_size = (450, 75)
    sound_button_image = pygame.transform.scale(sound_button_image, new_button_size)
    instructions_button_image = pygame.transform.scale(instructions_button_image, instruction_button_size)
    resume_button_image = pygame.transform.scale(resume_button_image, new_button_size)

    SOUND_BUTTON = Button(image=sound_button_image, pos=(360, 250),
                         text_input="Sound", font=get_font(35), base_color="#d7fcd4", hovering_color="White",
                         action=toggle_sound)
    INSTRUCTIONS_BUTTON = Button(image=instructions_button_image, pos=(360, 350),
                                text_input="Instructions", font=get_font(35), base_color="#d7fcd4",
                                hovering_color="White", action=show_instructions)
    RESUME_BUTTON = Button(image=resume_button_image, pos=(360, 450),
                           text_input="Resume", font=get_font(35), base_color="#d7fcd4", hovering_color="White",
                           action=resume_game)

    pause_menu_buttons = [SOUND_BUTTON, INSTRUCTIONS_BUTTON, RESUME_BUTTON]

def show_pause_menu():
    global pause_menu_buttons
    screen.blit(background, (0, 0))

    PAUSE_TEXT = get_font(40).render("PAUSED", True, "#b68f40")
    PAUSE_RECT = PAUSE_TEXT.get_rect(center=(360, 100))
    screen.blit(PAUSE_TEXT, PAUSE_RECT)

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    for button in pause_menu_buttons:
        button.changeColor(MENU_MOUSE_POS)
        button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in pause_menu_buttons:
                if button.checkForInput(MENU_MOUSE_POS):
                    button.action()

    pygame.display.update()   

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
