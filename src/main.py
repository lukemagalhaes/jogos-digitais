import pygame
import sys
from pygame.locals import *
from bullet import Bullet
from healthBar import HealthBar
from menu import Button
from player import Player
from adversary import Adversary

W, H = 720, 720
FPS = 60
current_phase = 1 

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

adversary = Adversary(350, 415, 3, 100)
adversary.image = pygame.transform.scale(adversary.image, (350, 350))
adversarys.add(adversary)

player_health_bar = HealthBar(10, 15, 200, 20, 100, is_player=True)
adversary_health_bar = HealthBar(W - 210, 15, 200, 20, 100, is_player=False)

shoot_delay = 300
last_shoot_time = pygame.time.get_ticks()

score = 0
paused = False
pause_menu_buttons = []
sound_enabled = True
sound_text = "on"

def initialize_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/heroesTheme.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound("assets/sounds/fire.wav")

initialize_sound()

def show_instructions():
    global paused
    paused = True

    instructions_text = (
        "Instruções:\n"
        "Setas: andar\n"
        "Barra de Espaço: Pular\n"
        "Botão esquerdo do mouse: Atirar\n"
        "ESC: Pausar/Continuar"
    )

    font = get_font(20)
    
    lines = instructions_text.split('\n')

    total_height = len(lines) * font.get_height()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

        screen.fill((30, 90, 120))

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, (255, 255, 255))
            line_rect = line_surface.get_rect(center=(W // 2, (H - total_height) // 2 + i * font.get_height()))
            screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)

def toggle_sound():
    global sound_enabled
    global sound_text
    if sound_enabled:
        pygame.mixer.music.stop()
        sound_text = "off"
    else:
        pygame.mixer.music.play(-1)  
        sound_text = "on"
    sound_enabled = not sound_enabled
    create_pause_menu_buttons()

def resume_game():
    global paused
    paused = False

def game_over():
    global score
    running_game_over = True

    while running_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_RETURN:
                    score = 0 
                    player.reset()  
                    
                    main_menu() 

        screen.fill((0, 0, 0))  

        game_over_font = get_font(60)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(W // 2, H // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        score_font = get_font(40)
        score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(W // 2, H // 2 + 50))
        screen.blit(score_text, score_rect)

        press_enter_text = get_font(15).render("Pressione Enter para retornar ao menu principal", True, (255, 255, 255))
        press_enter_rect = press_enter_text.get_rect(center=(W // 2, H - 50))
        screen.blit(press_enter_text, press_enter_rect)

        pygame.display.flip()
        clock.tick(FPS)


def create_pause_menu_buttons():
    global pause_menu_buttons

    sound_button_image = pygame.image.load("assets/menu/Play Rect.png")
    instructions_button_image = pygame.image.load("assets/menu/Play Rect.png")
    resume_button_image = pygame.image.load("assets/menu/Play Rect.png")

    new_button_size = (345, 75)
    instruction_button_size = (450, 75)
    sound_button_image = pygame.transform.scale(sound_button_image, new_button_size)
    instructions_button_image = pygame.transform.scale(instructions_button_image, instruction_button_size)
    resume_button_image = pygame.transform.scale(resume_button_image, new_button_size)

    SOUND_BUTTON = Button(image=sound_button_image, pos=(360, 250),
                         text_input=f"Sound {sound_text}", font=get_font(35), base_color="#d7fcd4", hovering_color="White",
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

def play_next_phase():
    global current_phase, background, adversary

    if current_phase == 1:
        background = pygame.image.load('assets/background/level2.jpg')
        current_phase += 1
        adversarys.remove(adversary)
        player.fall(630)
        player.health = 100
        adversary = Adversary(400, 495, 7, 100)
        adversary.image = pygame.image.load('assets/adversary/furacao.png')
        adversary.image = pygame.transform.scale(adversary.image, (263, 365))
        adversarys.add(adversary)  
    elif current_phase == 2:
        background = pygame.image.load('assets/background/level3.jpg')
        adversarys.remove(adversary)
        player.fall(650)
        player.health = 100
        adversary = Adversary(400, 496, 10, 100)
        adversary.image = pygame.image.load('assets/adversary/tufao.png')
        adversary.image = pygame.transform.scale(adversary.image, (328, 417))
        adversarys.add(adversary)  

def play():
    global last_shoot_time, score, pause_menu_buttons, paused
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
                    shoot_sound.set_volume(1)
                    shoot_sound.play(1)
                    new_bullet = Bullet(player.rect.x, player.rect.y)
                    mouse_pos = pygame.mouse.get_pos()
                    new_bullet.shoot(mouse_pos)
                    bullets.add(new_bullet)
                    last_shoot_time = current_time
        player_health_bar.update(player.health)
        adversary_health_bar.update(adversary.health)
        screen.blit(player_health_bar.image, player_health_bar.rect)
        screen.blit(adversary_health_bar.image, adversary_health_bar.rect)



        if paused:
            show_pause_menu()
        else:
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
                    global score
                    score += 1

            if pygame.sprite.collide_mask(player, adversary):
                player.lose_health(1)

            players.update()
            players.draw(screen)

            bullets.update()

            for bullet in bullets:
                if not (0 <= bullet.rect.x <= W and 0 <= bullet.rect.y <= H):
                    bullet.kill()

            bullets.draw(screen)

            adversarys.draw(screen)
            screen.blit(player_health_bar.image, player_health_bar.rect)
            screen.blit(adversary_health_bar.image, adversary_health_bar.rect)

            if player.health <= 0:
                game_over()
                return False
        
            show_score() 
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
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    QUIT_BUTTON.action()
        pygame.display.update()

def show_score():
    score_font = get_font(28)
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(W // 2, 25))
    screen.blit(score_text, score_rect)

if __name__ == "__main__":
    main_menu()
