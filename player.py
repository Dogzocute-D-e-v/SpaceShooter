import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/spaceship.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.max_health = 3
        self.health = self.max_health

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width:
            self.x += self.speed

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def is_dead(self):
        return self.health <= 0