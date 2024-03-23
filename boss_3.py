import pygame
from fireball import Fireball

screen_width = 1000
screen_height = 800


class BossThree(pygame.sprite.Sprite):
    def __init__(self, screen, image_sheet, position, all_sprites_group, fireballs_group):
        super().__init__()
        self.image_sheet = image_sheet
        self.screen = screen  # Сохраняем screen как атрибут класса
        self.images = {
            'normal': self.image_sheet.subsurface((0, 0, 240, 265)),
            'hit': self.image_sheet.subsurface((260, 0, 230, 260))
        }
        self.image = self.images['normal']
        self.rect = self.image.get_rect(topleft=position)
        self.all_sprites = all_sprites_group
        self.fireballs = fireballs_group
        self.health = 5  # Три жизни у босса
        self.hit_time = 0
        self.attack_frequency = 3000  # Частота атаки в миллисекундах
        self.last_attack = pygame.time.get_ticks()  # Время последней атаки

    def update(self):
        # Проверка состояния "попадание"
        if pygame.time.get_ticks() - self.hit_time > 1000:  # Если прошла 1 секунда после попадания
            self.image = self.images['normal']
        # Дополнительная логика обновления (например, стрельба)
        # Дополнительная логика обновления
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > self.attack_frequency:
            self.fire()
            self.last_attack = current_time

    def hit(self):  # Вызывается при попадании копья игрока
        self.health -= 0.5
        self.image = self.images['hit']
        self.hit_time = pygame.time.get_ticks()  # Запоминаем время попадания
        if self.health <= 0:
            self.kill()  # Удаление босса при смерти
            self.show_level_complete()  # Показываем сообщение о завершении уровня

    def show_level_complete(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Level complete", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(5000)
        global current_screen, in_game
        current_screen = "menu"
        in_game = False

    def fire(self):
        # Запуск шарика в сторону игрока
        fireball = Fireball(self.rect.midtop)
        self.fireballs.add(fireball)
        self.all_sprites.add(fireball)