import pygame
import sys
import random

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
PLAYER_HEALTH = 100
PLAYER_LIVES = 3

# Enemy settings
ENEMY_SPEED = 3
ENEMY_HEALTH = 50

# Projectile settings
BULLET_SPEED = 10
BULLET_DAMAGE = 20

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.health = PLAYER_HEALTH
        self.lives = PLAYER_LIVES

    def update(self):
        self.acc = pygame.math.Vector2(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pygame.K_DOWN]:
            self.acc.y = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.acc.y += self.vel.y * PLAYER_FRICTION

        self.vel += self.acc
        self.rect.x += self.vel.x + 0.5 * self.acc.x
        self.rect.y += self.vel.y + 0.5 * self.acc.y

        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel.y = 0
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.vel.y = 0

    def jump(self):
        self.vel.y = -PLAYER_JUMP

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red color for enemies
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)  # Randomize initial y position
        self.vel = pygame.math.Vector2(-ENEMY_SPEED, 0)
        self.health = ENEMY_HEALTH

    def update(self):
        self.rect.x += self.vel.x
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)  # Randomize position when reaching edge


class InterferenceEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow color for interference enemies
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)  # Randomize initial y position
        self.vel = pygame.math.Vector2(-ENEMY_SPEED, 0)

    def update(self):
        self.rect.x += self.vel.x
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)  # Randomize position when reaching edge


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = pygame.math.Vector2(BULLET_SPEED, 0)

    def update(self):
        self.rect.x += self.vel.x
        if self.rect.left > WIDTH:
            self.kill()


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
enemies = pygame.sprite.Group()
interference_enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def main():
    running = True
    enemy_spawn_counter = 0  # Counter for enemy spawning
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_z:
                    player.shoot()

        all_sprites.update()

        # Spawn a new red block enemy every few frames
        enemy_spawn_counter += 1
        if enemy_spawn_counter >= FPS * 3:  # Adjust the number of frames here for the spawning rate
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_spawn_counter = 0  # Reset counter after spawning

        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            player.health -= 10
            if player.health <= 0:
                player.lives -= 1
                if player.lives <= 0:
                    # Game over
                    game_over()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit_enemy in hits.values():
            for enemy in hit_enemy:
                # Add score increment here if needed
                pass

        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def game_over():
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()


if __name__ == "__main__":
    # Adding interference enemies
    for _ in range(3):
        interference_enemy = InterferenceEnemy()
        all_sprites.add(interference_enemy)

    main()



# Github Link --------------------( https://github.com/fn1ashish/Assignment-3.git )---------------------------