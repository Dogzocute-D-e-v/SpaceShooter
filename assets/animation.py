import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution Triangles")

WHITE = (255, 255, 255)
clock = pygame.time.Clock()

def random_color():
    return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

def random_direction():
    return random.choice([-1, 1])

def random_speed():
    return random.randint(2, 4)

class MovingObject:
    def __init__(self, x, y, size, shape, baby=True):
        self.x = x
        self.y = y
        self.size = size
        self.shape = shape
        self.color = random_color()
        self.dir_x = random_direction()
        self.dir_y = random_direction()
        self.speed = random_speed()
        self.alive = True
        self.baby = baby

    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.dir_x *= -1
        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.dir_y *= -1

    def draw(self, surface):
        if self.shape == "circle":
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        elif self.shape == "square":
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        elif self.shape == "triangle":
            half = self.size // 2
            points = [
                (self.x + half, self.y),
                (self.x, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ]
            pygame.draw.polygon(surface, self.color, points)

    def get_rect(self):
        if self.shape == "circle":
            return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        return pygame.Rect(self.x, self.y, self.size, self.size)

def check_collision(obj1, obj2):
    return obj1.get_rect().colliderect(obj2.get_rect())

circle = MovingObject(150, 150, 25, "circle", baby=False)
square = MovingObject(400, 250, 40, "square", baby=False)
baby_triangles = []
full_triangles = []
triangle_collision_count = 0

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    circle.move()
    square.move()

    if check_collision(circle, square):
        circle.color = random_color()
        square.color = random_color()
        circle.dir_x *= -1
        circle.dir_y *= -1
        square.dir_x *= -1
        square.dir_y *= -1
        baby_triangles.append(MovingObject((circle.x + square.x) // 2, (circle.y + square.y) // 2, 15, "triangle", baby=True))

    for tri in baby_triangles:
        tri.move()

    for tri in full_triangles:
        tri.move()

    for i in range(len(baby_triangles)):
        for j in range(i + 1, len(baby_triangles)):
            t1 = baby_triangles[i]
            t2 = baby_triangles[j]
            if t1.alive and t2.alive and check_collision(t1, t2):
                triangle_collision_count += 1
                t1.dir_x *= -1
                t1.dir_y *= -1
                t2.dir_x *= -1
                t2.dir_y *= -1
                t1.alive = False
                t2.alive = False
                if triangle_collision_count >= 5:
                    full_triangles.append(MovingObject((t1.x + t2.x) // 2, (t1.y + t2.y) // 2, 30, "triangle", baby=False))
                    triangle_collision_count = 0
                break

    baby_triangles = [t for t in baby_triangles if t.alive]

    circle.draw(screen)
    square.draw(screen)

    for tri in baby_triangles:
        tri.draw(screen)
    for tri in full_triangles:
        tri.draw(screen)

    pygame.display.flip()
    clock.tick(60)
