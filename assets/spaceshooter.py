import pygame
import random
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter: Animated Background Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (100, 200, 255)
GREEN = (50, 255, 100)
YELLOW = (255, 255, 80)

player_img = pygame.image.load("assets/avatar.png")
player_img = pygame.transform.scale(player_img, (50, 50))
player_x = WIDTH // 2
player_y = HEIGHT - 70
player_speed = 5
player_health = 3

score = 0
game_over = False

bullets = []
bullet_speed = -8

enemies = []
enemy_timer = 0
enemy_delay = 30
enemy_speed = 2

circle = {'x': 100, 'y': 100, 'dx': 3, 'dy': 2, 'r': 30, 'color': RED}
square = {'x': 300, 'y': 200, 'dx': -2, 'dy': 3, 'size': 40, 'color': GREEN}
triangles = []
triangle_collisions = 0

def spawn_triangle(x, y):
    triangles.append({'x': x, 'y': y, 'size': 10, 'grown': False})

def draw_triangle(x, y, size):
    points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
    pygame.draw.polygon(win, YELLOW, points)

def background_animate():
    global triangle_collisions
    circle['x'] += circle['dx']
    circle['y'] += circle['dy']
    if circle['x'] < circle['r'] or circle['x'] > WIDTH - circle['r']:
        circle['dx'] *= -1
    if circle['y'] < circle['r'] or circle['y'] > HEIGHT - circle['r']:
        circle['dy'] *= -1

    square['x'] += square['dx']
    square['y'] += square['dy']
    if square['x'] < 0 or square['x'] > WIDTH - square['size']:
        square['dx'] *= -1
    if square['y'] < 0 or square['y'] > HEIGHT - square['size']:
        square['dy'] *= -1


    if (square['x'] < circle['x'] < square['x'] + square['size']) and \
       (square['y'] < circle['y'] < square['y'] + square['size']):
        circle['color'], square['color'] = square['color'], circle['color']
        spawn_triangle((circle['x'] + square['x']) // 2, (circle['y'] + square['y']) // 2)

    # Move Triangles
    for t in triangles:
        t['y'] += 1
    for i, t1 in enumerate(triangles):
        for j, t2 in enumerate(triangles):
            if i != j and not t1['grown'] and not t2['grown']:
                dist = math.hypot(t1['x'] - t2['x'], t1['y'] - t2['y'])
                if dist < 20:
                    t1['size'] = t2['size'] = 20
                    t1['grown'] = t2['grown'] = True
                    triangle_collisions += 1

    pygame.draw.circle(win, circle['color'], (int(circle['x']), int(circle['y'])), circle['r'])
    pygame.draw.rect(win, square['color'], (square['x'], square['y'], square['size'], square['size']))
    for t in triangles:
        draw_triangle(t['x'], t['y'], t['size'])

def draw_player():
    win.blit(player_img, (player_x, player_y))

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(win, BLUE, enemy)

def draw_bullets():
    for b in bullets:
        pygame.draw.rect(win, WHITE, b)

def check_collisions():
    global score
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

def reset_game():
    global bullets, enemies, score, player_health, triangle_collisions, triangles, game_over
    bullets.clear()
    enemies.clear()
    triangles.clear()
    triangle_collisions = 0
    player_health = 3
    score = 0
    game_over = False

def game_loop():
    global player_x, bullets, enemies, enemy_timer, player_health, game_over

    running = True
    while running:
        clock.tick(60)
        win.fill((10, 10, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_over:
            background_animate()

            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
                player_x += player_speed
            if keys[pygame.K_SPACE]:
                if len(bullets) < 5:
                    bullets.append(pygame.Rect(player_x + 23, player_y, 4, 10))

            for b in bullets:
                b.y += bullet_speed
            bullets = [b for b in bullets if b.y > 0]

            enemy_timer += 1
            if enemy_timer >= enemy_delay:
                enemy_timer = 0
                ex = random.randint(0, WIDTH - 40)
                enemies.append(pygame.Rect(ex, -30, 40, 30))

            for e in enemies:
                e.y += enemy_speed

            for enemy in enemies[:]:
                if enemy.colliderect(pygame.Rect(player_x, player_y, 50, 50)):
                    enemies.remove(enemy)
                    player_health -= 1
                elif enemy.y > HEIGHT:
                    enemies.remove(enemy)
                    player_health -= 1

            if player_health <= 0:
                game_over = True

            draw_player()
            draw_bullets()
            draw_enemies()
            check_collisions()

            win.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
            win.blit(font.render(f"Triangle Evolutions: {triangle_collisions}", True, WHITE), (10, 40))
            win.blit(font.render(f"Health: {player_health}", True, RED), (10, 70))

        else:
            win.fill((0, 0, 0))
            text = font.render("GAME OVER! Press R to Restart or Q to Quit", True, RED)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

            if keys[pygame.K_r]:
                reset_game()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    pygame.quit()

game_loop()
