import pygame


class Spear(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            'spear.png')  # Убедитесь, что у вас есть файл изображения под названием "spear.png" в нужной директории
        self.rect = self.image.get_rect(center=position)
        self.velocity = 1  # Скорость, с которой копьё будет двигаться вправо. Можете изменить в зависимости от нужд игры

    def update(self):
        self.rect.x += self.velocity  # Движение копья вправо
        if self.rect.left > 1000:  # Если копьё выходит за пределы экрана, оно удаляется. 1000 - это ширина окна вашей игры, возможно, вам потребуется её изменить
            self.kill()  # Удаление спрайта, когда он выходит за пределы экрана
