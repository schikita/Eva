import pygame


class Fireball(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # Красный цвет
        # Модифицируем позицию для смещения вниз на 50 пикселей
        adjusted_position = (position[0], position[1] + 80)
        self.rect = self.image.get_rect(center=adjusted_position)
        self.velocity = -0.6  # Шарики летят влево

    def update(self):
        self.rect.x += self.velocity
        # Удаляем шарик, если он выходит за пределы экрана
        if self.rect.right < 0:
            self.kill()
