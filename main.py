import pygame
import sys
from player import Player
from spear import Spear
from boss import Boss
from fireball import Fireball

# Инициализация Pygame
pygame.init()

# Основные настройки экрана
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Evangelion")

# Инициализация групп спрайтов
all_sprites = pygame.sprite.Group()
spears = pygame.sprite.Group()

# Загрузка изображения листа спрайтов и создание игрока
player_image_sheet = pygame.image.load('Sprite-player-1.png')
player = Player(player_image_sheet, (100, 100), all_sprites, spears, screen_height)

all_sprites.add(player)

fireballs = pygame.sprite.Group()

# Загрузка спрайтового листа босса
boss_image_sheet = pygame.image.load('Boss-1.png').convert_alpha()
boss_position = (screen_width - 300, screen_height - 260)  # Учитывая, что размер спрайта босса - 250x250

# Создание экземпляра босса
boss = Boss(screen, boss_image_sheet, boss_position, all_sprites, fireballs)

# Добавление босса в группу всех спрайтов
all_sprites.add(boss)

# Иконка игры
programIcon = pygame.image.load('Icon-1.png')
pygame.display.set_icon(programIcon)

# Фон и музыка для первоначального меню
menu_background_image = pygame.image.load('Start-game-1.png')
pygame.mixer.music.load('04-Cruel-Angel_s-Thesis.ogg')
pygame.mixer.music.play(-1)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифты
font = pygame.font.Font(None, 36)

# Переменные состояния игры
current_screen = "menu"
selected_option = 0
pause_selected_option = 0
in_game = False
pause_options = ["Continue", "Mute", "Exit"]
menu_options = ["Level 1", "Level 2", "Level 3", "Intro", "Mute", "Exit"]
music_muted = False

# Фоновые изображения и музыка для каждого уровня
backgrounds = {
    "Level 1": "BG-Level-1.png",
    "Level 2": "BG_levels_2.png",
    "Level 3": "BG-level-3.png",
}
music_files = {
    "Level 1": "08-Angel-Attack.ogg",
    "Level 2": "12-EVA-00.ogg",
    "Level 3": "23-The-Beast.ogg",
}
current_background = None
current_music = None

level_1_completed = False
level_2_completed = False
level_3_completed = False


def toggle_music():
    global music_muted
    music_muted = not music_muted
    if music_muted:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


def load_level(level):
    global current_background, current_music, in_game, boss
    current_background = pygame.image.load(backgrounds[level])
    current_music = music_files[level]
    pygame.mixer.music.load(current_music)
    pygame.mixer.music.play(-1)
    in_game = True

    # Предполагаем, что boss объявлен как None или уже создан где-то в начале
    if level == "Level 1":
        # Создание и добавление босса только для первого уровня
        if boss is None:  # Создаем босса, если он еще не создан
            boss = Boss(boss_image_sheet, boss_position, all_sprites, fireballs)
            all_sprites.add(boss)
        else:
            boss.rect.topleft = boss_position  # Перемещаем босса на его позицию, если он уже существует
    else:
        # Удаляем босса из всех групп спрайтов, если это не первый уровень
        if boss:
            boss.kill()
            boss = None  # Сброс boss в None после удаления


def draw_level():
    screen.blit(current_background, (0, 0))


def process_menu_selection(option):
    global current_screen, in_game, running
    if option in ["Level 1", "Level 2", "Level 3"]:
        load_level(option)
        current_screen = option
        in_game = True
    elif option == "Mute":
        toggle_music()
    elif option == "Exit":
        running = False


def process_pause_selection(option):
    global current_screen, in_game, running
    if option == "Continue":
        current_screen = "game"
        in_game = True
    elif option == "Mute":
        toggle_music()
    elif option == "Exit":
        current_screen = "menu"
        in_game = False
        selected_option = 0
        pygame.mixer.music.stop()
        pygame.mixer.music.load('04-Cruel-Angel_s-Thesis.ogg')
        pygame.mixer.music.play(-1)


def draw_menu(options, selected):
    screen.blit(menu_background_image, (0, 0))
    menu_x = screen_width * 3 / 4
    for i, option in enumerate(options):
        if i == 0 and level_1_completed:  # Если это первый уровень и он завершен
            color = (100, 100, 100)  # Серый цвет для неактивного пункта
        else:
            color = WHITE if i == selected else (100, 100, 100)
        text = font.render(option, True, color)
        screen.blit(text, (menu_x - text.get_width() / 2, 150 + 50 * i))


def main():
    global current_screen, selected_option, pause_selected_option, in_game, music_muted, boss

    running = True
    level_complete = False  # Флаг завершения уровня

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and in_game:
                    current_screen = "pause"
                    continue

                if current_screen == "menu":
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        process_menu_selection(menu_options[selected_option])

                elif current_screen == "pause":
                    if event.key == pygame.K_DOWN:
                        pause_selected_option = (pause_selected_option + 1) % len(pause_options)
                    elif event.key == pygame.K_UP:
                        pause_selected_option = (pause_selected_option - 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN:
                        process_pause_selection(pause_options[pause_selected_option])

        keys = pygame.key.get_pressed()
        screen.fill(BLACK)

        if current_screen == "menu":
            draw_menu(menu_options, selected_option)
        elif current_screen == "pause":
            draw_menu(pause_options, pause_selected_option)
        elif in_game:
            draw_level()
            player.update(keys)  # Обновление игрока с передачей клавиш

            fireballs.update()

            # Обновляем спрайты, исключая игрока, если в группе all_sprites есть и другие спрайты
            for sprite in all_sprites:
                if sprite != player:
                    sprite.update()

            spears.update()

            all_sprites.draw(screen)
            spears.draw(screen)
            fireballs.draw(screen)



            # Проверка столкновений
            if boss is not None and boss.alive():  # Добавлена проверка на существование объекта boss
                hits = pygame.sprite.spritecollide(boss, spears, True)
                for hit in hits:
                    boss.hit()
                    if boss.health <= 0:  # Проверяем здоровье босса после попадания
                        level_complete = True
                        display_time = pygame.time.get_ticks()
                        boss.kill()  # Удаляем босса из всех групп спрайтов
                        level_1_completed = True  # Указываем, что первый уровень завершен

            # Показываем сообщение "Level Complete", если уровень завершен
            if level_complete:
                if pygame.time.get_ticks() - display_time < 5000:  # Отображаем сообщение в течение 5 секунд
                    font = pygame.font.Font(None, 74)
                    text = font.render('Level Complete', True, WHITE)
                    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
                    screen.blit(text, text_rect)
                else:
                    # Возвращение в главное меню после 5 секунд
                    current_screen = "menu"
                    in_game = False
                    level_complete = False  # Сброс флага завершения уровня для возможного повторного прохождения

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
