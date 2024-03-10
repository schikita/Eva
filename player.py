import pygame
from spear import Spear

screen_height = 800


class Player(pygame.sprite.Sprite):
    def __init__(self, image_sheet, position, all_sprites_group, spears_group, screen_height):
        super().__init__()
        super().__init__()
        self.screen_height = screen_height
        self.image_sheet = image_sheet
        self.all_sprites = all_sprites_group
        self.spears = spears_group
        self.last_direction = "right"
        self.state = "standing"
        self.anim_index = 0
        self.anim_timer = pygame.time.get_ticks()
        self.velocity = 5
        self.jump_speed = -20
        self.gravity = 0.3
        self.on_ground = True
        self.y_velocity = 0
        self.frame_rects = {  # Словарь теперь является атрибутом экземпляра
            "standing": [(0, 0, 150, 150)],
            "running_forward": [(150, 0, 150, 150), (300, 0, 150, 150)],
            "running_backward": [(150, 150, 150, 150), (300, 150, 150, 150)],
            "backward_standing": [(0, 150, 150, 150)],
            "jumping_forward": [(0, 300, 150, 150)],
            "jumping_backward": [(0, 450, 150, 150)],
            "crouching_forward": [(0, 340, 150, 110)],
            "crouching_backward": [(0, 300, 150, 150)],
            "attacking_forward": [(150, 300, 150, 150)],
            "attacking_backward": [(150, 450, 150, 150)],
        }
        self.update_rect(position)
        self.health = 5  # Начальное количество жизней

    def update_rect(self, position):
        frame_rects = {
            "standing": (0, 0, 150, 150),
            "running_forward": [(150, 0, 150, 150), (300, 0, 150, 150)],
            "running_backward": [(150, 150, 150, 150), (300, 150, 150, 150)],
            "backward_standing": (0, 150, 150, 150),
            "jumping_forward": (0, 300, 150, 150),
            "jumping_backward": (0, 450, 150, 150),
            "crouching_forward": (0, 340, 150, 110),
            "crouching_backward": (0, 300, 150, 150),
            "attacking_forward": (150, 300, 150, 150),
            "attacking_backward": (150, 450, 150, 150),
        }
        frame = frame_rects[self.state][self.anim_index] if isinstance(frame_rects[self.state], list) else frame_rects[
            self.state]
        self.image = self.image_sheet.subsurface(frame)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self, keys):
        current_time = pygame.time.get_ticks()
        if self.on_ground:
            if keys[pygame.K_LEFT]:
                self.move(-self.velocity, "running_backward")
            elif keys[pygame.K_RIGHT]:
                self.move(self.velocity, "running_forward")
            elif keys[pygame.K_DOWN]:
                self.crouch()
            elif keys[pygame.K_SPACE]:
                self.throw_spear()
            elif keys[pygame.K_UP]:
                self.jump()
            else:
                self.stand()

        self.apply_gravity()

    def move(self, velocity, state):
        self.rect.x += velocity
        self.state = state
        self.last_direction = "right" if velocity > 0 else "left"
        self.update_animation()

    def crouch(self):
        self.state = "crouching_forward" if self.last_direction == "right" else "crouching_backward"
        self.update_animation()

    def stand(self):
        self.state = "standing"
        self.update_animation()

    def jump(self):
        if self.on_ground:
            self.y_velocity = self.jump_speed
            self.on_ground = False
            self.state = "jumping_forward" if self.last_direction == "right" else "jumping_backward"
            self.anim_index = 0  # Сброс анимации
            self.update_animation()

    def apply_gravity(self):
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity
        if self.rect.bottom > 750:
            self.rect.bottom = 750
            self.on_ground = True
            self.y_velocity = 0

        # Плавное замедление перед приземлением
        if self.rect.bottom >= screen_height - 100 and self.y_velocity > 0:  # Если персонаж находится на высоте 100px от земли и движется вниз
            self.y_velocity *= 0.8  # Замедляем скорость падения

        # Проверка приземления на землю
        if self.rect.bottom > screen_height - 50:
            self.rect.bottom = screen_height - 50
            self.on_ground = True
            self.y_velocity = 0

    def throw_spear(self):
        if not self.state.startswith('attacking'):
            spear = Spear((self.rect.centerx + (50 if self.last_direction == "right" else -50), self.rect.centery))
            self.all_sprites.add(spear)
            self.spears.add(spear)
            self.state = "attacking_forward" if self.last_direction == "right" else "attacking_backward"
            self.update_animation()

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.anim_timer > 100:
            self.anim_index = (self.anim_index + 1) % len(self.frame_rects[self.state])
            self.anim_timer = current_time
            self.update_rect(self.rect.topleft)

    def take_damage(self):
        self.health -= 1
        # Загрузка и установка спрайта игрока, соответствующего получению урона
        damage_frame = self.image_sheet.subsurface((0, 600, 150, 150))  # Выбираем часть спрайта
        self.image = damage_frame
        if self.health <= 0:
            self.die()
        else:
            # Возвращаем оригинальный спрайт через 0.5 секунды
            pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Используем пользовательское событие для задержки

    def die(self):
        # Обработка смерти игрока
        global current_screen
        current_screen = "menu"
        # Отображение сообщения "You lose" можно сделать здесь или в главном цикле
