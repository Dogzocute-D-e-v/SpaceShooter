import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, img=None):
        self.images = [
            pygame.image.load("assets/enemy1.png")
            # pygame.image.load("assets/enemy2.png"),
            # pygame.image.load("assets/enemy3.png")
        ]
        self.image = img if img else pygame.transform.scale(random.choice(self.images), (40, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_y = 0.7
        self.wave_offset = random.uniform(0, math.pi * 2)

    def update(self, tick):
        # Horizontal wave movement
        wave_x = math.sin(tick / 20 + self.wave_offset) * 1.5
        self.rect.x += wave_x
        self.rect.y += self.speed_y

    def draw(self, win):
        win.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.y > 600

    def collides_with_player(self, px, py, pw, ph):
        player_rect = pygame.Rect(px, py, pw, ph)
        return self.rect.colliderect(player_rect)

def generate_formation(form_type="line", max_enemies=30):
    formation = []
    base_x = random.randint(100, 600)
    base_y = -50
    spacing = 50
    if form_type == "line":
        for i in range(min(5, max_enemies)):
            formation.append(Enemy(base_x + i * spacing, base_y))
    elif form_type == "v":
        v_shape = [
            (0, 0), (spacing, spacing), (2 * spacing, 2 * spacing),
            (spacing * 2, spacing), (spacing, 0)
        ]
        for i, (dx, dy) in enumerate(v_shape):
            if len(formation) >= max_enemies:
                break
            formation.append(Enemy(base_x + dx, base_y + dy))
    elif form_type == "box":
        for row in range(2):
            for col in range(3):
                if len(formation) >= max_enemies:
                    break
                formation.append(Enemy(base_x + col * spacing, base_y + row * spacing))
    else:
        formation.append(Enemy(base_x, base_y))
    return formation