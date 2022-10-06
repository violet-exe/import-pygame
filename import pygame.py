import pygame
import random
import os

FPS = 60

W=500
H=600

WHITE=(255,255,255)
PURPLE=(120,10,230)
BLACK=(0,0,0)
BLUE=(0,220,200)

pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("早ㄤ")
clock = pygame.time.Clock()
GREEN=(0,255,0)

#載入圖片

background_img = pygame.image.load(os.path.join("img" , "background.png")).convert()
player_img = pygame.image.load(os.path.join("img" , "player.png")).convert()
rock_img = pygame.image.load(os.path.join("img" , "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img" , "bullet.png")).convert()


#船-----------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img , (50,38))
        self.image.set_colorkey(BLACK)
        #self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx=W/2
        self.rect.bottom = H-50
        self.speedx = 8
        
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
            
        if self.rect.right > W:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx , self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
#石頭---------------------------------        
        
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.image.set_colorkey(BLACK)
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,W - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > H or self.rect.left > W or self.rect.right < 0:
            self.rect.x = random.randrange(0,W - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,10)
            self.speedx = random.randrange(-3,3)

#子彈-----------------------------------------

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
                
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 :
            self.kill()
            
#

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)
    
    
#遊戲迴圈
running=True
while running :
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            
#更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
        
    hits = pygame.sprite.spritecollide(player, rocks, False)
    if hits:
        running = False

#畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img , (0,0))
    all_sprites.draw(screen)
    pygame.display.update()

#

pygame.quit()
