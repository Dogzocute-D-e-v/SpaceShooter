import pygame

class EnemyBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 18, y + 30, 6, 12)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), self.rect)

    def off_screen(self, height):
        return self.rect.y > height