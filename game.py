import pygame
import random
import sys
from player import Player
from enemy import generate_formation, Enemy
from bullet import Bullet
from enemy_bullet import EnemyBullet
from utils import save_score, load_score, get_special_ability, activate_ability, update_ability_timer

WIDTH, HEIGHT = 800, 600

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.player = Player(WIDTH // 2, HEIGHT - 70)
        self.bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.score = 0
        self.high_score = load_score()

        self.ability = get_special_ability()
        self.enemy_spawn_delay = 60  # slowed spawn
        self.enemy_timer = 0
        self.last_shot_time = 0
        self.bullet_delay = 400  # milliseconds
        self.tick_count = 0

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            self.tick_count += 1
            self.win.fill((255, 255, 255))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_score(max(self.score, self.high_score))
                    running = False

            if not self.player.is_dead():
                self.player.move(keys, WIDTH)

                if keys[pygame.K_1]:
                    activate_ability(self.ability, "nuke")
                if keys[pygame.K_2]:
                    activate_ability(self.ability, "shield")
                if keys[pygame.K_3]:
                    activate_ability(self.ability, "rapid_fire")

                if self.ability["nuke"]:
                    self.enemies.clear()
                    self.ability["nuke"] = False

                update_ability_timer(self.ability, dt)

                cooldown = 100 if self.ability["rapid_fire"] else self.bullet_delay
                if keys[pygame.K_SPACE] and pygame.time.get_ticks() - self.last_shot_time > cooldown:
                    self.bullets.append(Bullet(self.player.x + 23, self.player.y))
                    self.last_shot_time = pygame.time.get_ticks()

                for bullet in self.bullets:
                    bullet.update()
                self.bullets = [b for b in self.bullets if not b.off_screen()]

                self.enemy_timer += 1
                if self.enemy_timer >= self.enemy_spawn_delay:
                    self.enemy_timer = 0
                    formation_type = random.choice(["line", "v", "box"])
                    self.enemies.extend(generate_formation(formation_type, max_enemies=1))

                for enemy in self.enemies[:]:
                    enemy.update(self.tick_count)
                    if random.randint(0, 500) < 1:

                        self.enemy_bullets.append(EnemyBullet(enemy.rect.x, enemy.rect.y))

                    if enemy.collides_with_player(self.player.x, self.player.y, self.player.width, self.player.height):
                        self.enemies.remove(enemy)
                        if not self.ability["shield"]:
                            self.player.health -= 1
                        continue

                    for bullet in self.bullets:
                        if enemy.rect.colliderect(bullet.rect):
                            self.enemies.remove(enemy)
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                            self.score += 1
                            break

                    if enemy.off_screen():
                        self.enemies.remove(enemy)
                        if not self.ability["shield"]:
                            self.player.health -= 1

                for eb in self.enemy_bullets[:]:
                    eb.update()
                    if eb.off_screen(HEIGHT):
                        self.enemy_bullets.remove(eb)
                    elif eb.rect.colliderect(pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)):
                        if not self.ability["shield"]:
                            self.player.health -= 1
                        self.enemy_bullets.remove(eb)

            else:
                text = self.font.render("GAME OVER! Press R to Restart", True, (255, 0, 0))
                self.win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
                if keys[pygame.K_r]:
                    self.__init__()

            self.player.draw(self.win)
            for bullet in self.bullets:
                bullet.draw(self.win)
            for enemy in self.enemies:
                enemy.draw(self.win)
            for eb in self.enemy_bullets:
                eb.draw(self.win)

            self.draw_health_bar()
            self.draw_score()
            self.draw_active_ability()
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}  High: {self.high_score}", True, (0, 0, 0))
        self.win.blit(text, (10, 10))

    def draw_health_bar(self):
        bar_width = 200
        bar_height = 20
        x, y = 10, 40
        fill = (self.player.health / self.player.max_health) * bar_width
        pygame.draw.rect(self.win, (200, 200, 200), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.win, (255, 0, 0), (x, y, fill, bar_height))
        pygame.draw.rect(self.win, (0, 0, 0), (x, y, bar_width, bar_height), 2)

    def draw_active_ability(self):
        if self.ability["active"]:
            text = self.font.render(f"{self.ability['active'].upper()} ({self.ability['timer']:.1f}s)", True, (0, 0, 0))
            self.win.blit(text, (WIDTH - text.get_width() - 20, 10))