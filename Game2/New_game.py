import pygame
import random
import os

##pygame.mixer.init()
pygame.mixer.pre_init(16500, -16, 2, 2048)
pygame.init()
clock = pygame.time.Clock()

dodge = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

white = (255, 255, 255)
black = (0, 0, 0)
speed = 30


def things_dodged(count):
    font = pygame.font.SysFont("Consolas", 15)
    text = font.render("Dodged: "+str(count), True, black)
    screen.blit(text,(0,0))
    
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
        global dodge
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            dodge += 1
##            print(dodge)
            things_dodged(dodge)
            self.kill()


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Load and play Background Music
pygame.mixer.music.load("jazz.mp3")
pygame.mixer.music.play(loops = -1)

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
    things_dodged(dodge)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False


    pygame.display.flip()
    if pygame.time.get_ticks()%5000 <50:
        speed=speed+1
        #print(speed)
    clock.tick(speed)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
