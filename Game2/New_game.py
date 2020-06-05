import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

white = (255, 255, 255)
black = (0, 0, 0)
speed = 30

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey(white)
        self.rect = self.surf.get_rect(
                            center = (
                                    60, SCREEN_HEIGHT/2
                                )
                            )

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
                            center = (
                                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH +100),
                                    random.randint(0, SCREEN_HEIGHT)
                                )
                            )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.QUIT:
            running = False

        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    screen.fill((135, 206, 235))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False
    #surf = pygame.Surface((50, 50))
    #surf.fill(black)
    #rect = surf.get_rect()
    #screen.blit(player.surf, player.rect)
##    if start_time:
##        time_since_enter = pygame.time.get_ticks() - start_time
##        message = 'Milliseconds since enter: ' + str(time_since_enter)
##        screen.blit(FONT.render(message, True, TEXT_COLOR), (20, 20))
##    print(pygame.time.get_ticks())
    pygame.display.flip()
    if pygame.time.get_ticks()%5000 <50:
        speed=speed+1
        print(speed)
    clock.tick(speed)

pygame.quit()
