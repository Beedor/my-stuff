import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, self.rect.center, 20)
# Game class
class Game:
    def __init__(self):
# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, RED, self.rect.center, 15)

                                                                                                                                                                                                                                                                # Game class
                                                                                                                                                                                                                                                                class Game:
                                                                                                                                                                                                                                                                    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.score = 0
        self.enemy_spawn_timer = 0
        self.enemy_spawn_rate = 40
        self.enemy_speed = 3
        self.wave = 1
        self.game_over = False
        self.spawn_enemies_random()

    def spawn_enemies_random(self):
        for _ in range(2 + self.wave):
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = random.randint(-100, -30)
            speed = self.enemy_speed + (self.wave * 0.5)
            enemy = Enemy(x, y, speed)
            self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.game_over and event.key == pygame.K_SPACE:
                    return None  # Restart signal
        return True

    def update(self):
        if self.game_over:
            return

        self.player.update()

        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer > self.enemy_spawn_rate:
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = -30
            speed = self.enemy_speed + (self.wave * 0.5)
            self.enemies.append(Enemy(x, y, speed))
            self.enemy_spawn_timer = 0

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

        # Remove enemies that are off-screen
        self.enemies = [e for e in self.enemies if e.rect.top < SCREEN_HEIGHT]

        # Check for collisions
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True

        # Increase score
        self.score += 1

        # Increase difficulty
        if self.score % 500 == 0:
            self.wave += 1
            self.enemy_speed += 0.5
            self.enemy_spawn_rate = max(20, self.enemy_spawn_rate - 2)

    def draw(self):
        screen.fill(BLACK)

        # Draw player
        self.player.draw(screen)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {self.score // 10}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw wave
        wave_text = font.render(f"Wave: {self.wave}", True, YELLOW)
        screen.blit(wave_text, (SCREEN_WIDTH - 200, 10))

        # Draw controls
        controls = font.render("Arrow Keys: Move | ESC: Quit", True, WHITE)
        screen.blit(controls, (10, SCREEN_HEIGHT - 40))

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = large_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))

        # Final score
        final_score_text = font.render(f"Final Score: {self.score // 10}", True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 250))

        # Wave reached
        wave_text = font.render(f"Wave Reached: {self.wave}", True, YELLOW)
        screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 300))

        # Restart instruction
        restart_text = font.render("Press SPACE to Restart or ESC to Quit", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

# Main game loop
def main():
    running = True

    while running:
        game = Game()

        while running:
            result = game.handle_events()

            if result is None:  # Restart
                break
            elif result is False:  # Quit
                running = False
                break

            game.update()
            game.draw()
            clock.tick(60)  # 60 FPS
