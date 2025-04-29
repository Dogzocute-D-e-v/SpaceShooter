import pygame

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 4, 10)
        self.speed = -8

    def update(self):
        self.rect.y += self.speed

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), self.rect)

    def off_screen(self):
        return self.rect.y < 0