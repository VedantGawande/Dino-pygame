import pygame, sys, os, random

class Dino(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.GRAVITY = 10
        self.jump_h = y -170
        self.run_anim = False
        self.jump_anim = False
        self.duck_anim = False
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join('Assets\Dino', 'DinoJump.png')).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join('Assets\Dino', 'DinoRun1.png')).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join('Assets\Dino', 'DinoRun2.png')).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join('Assets\Dino', 'DinoDuck1.png')).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join('Assets\Dino', 'DinoDuck2.png')).convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.IN_AIR = False
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
    def run(self):
        self.run_anim = True
    
    def jump(self):
        self.jump_anim = True
    def duck(self):
        self.duck_anim = True
    def update(self, speed):
        self.rect.bottom += self.GRAVITY
        if self.run_anim:
            self.current_sprite += speed
            if int(self.current_sprite) >= 3:
                self.current_sprite = 1
                self.run_anim = False
        if self.duck_anim:
            print(len(self.sprites))
        if self.jump_anim:
            self.run_anim = False
            self.duck_anim = False
            self.current_sprite = 0
            while self.rect.centery != self.jump_h:
                self.rect.centery -= 1
            self.jump_anim = False
            self.run_anim = True
        
        if self.rect.bottom >= 357:            
            self.rect.bottom = 357
            self.IN_AIR = False
        else:
            self.IN_AIR = True
        if self.IN_AIR:
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
    def __init__(self, w, y, win):
        super().__init__()
        self.win = win
        self.x = 0
        self.y = y
        self.WIDTH = w
        self.base = pygame.image.load(os.path.join('Assets\Other', 'Track.png')).convert_alpha()
        self.rect = self.base.get_rect(center=(self.x, self.y))
    def move(self, speed):
        self.win.blit(self.base, self.rect)
        self.win.blit(self.base, (self.rect.centerx + self.base.get_width(), self.rect.centery))
        self.rect.centerx -= speed
        if self.rect.centerx <= 0:
            self.rect.centerx = self.WIDTH

class Cactus():
    def __init__(self, HEIGHT, win, WIDTH):
        super().__init__()
        self.win = win
        self.by = HEIGHT/2 +10 
        self.sy = HEIGHT/2 + 24
        self.x = WIDTH + 100
        self.var = [True, False]

        self.cactuses = []
        self.smallcactuses = []
        for i in range(4):
            if i != 0:
                self.cactuses.append(pygame.image.load(os.path.join('Assets\Cactus', f'LargeCactus{i}.png')).convert_alpha())
        for i in range(4):
            if i != 0:
                self.smallcactuses.append(pygame.image.load(os.path.join('Assets\Cactus', f'SmallCactus{i}.png')).convert_alpha())
    def big_small(self):
        if random.choice(self.var) == True:
            self.random_cactus = random.choice(self.cactuses)
            self.cactus_rect = self.random_cactus.get_rect(center = (self.x, self.by))
        else:
            self.random_cactus = random.choice(self.smallcactuses)
            self.cactus_rect = self.random_cactus.get_rect(center = (self.x, self.sy))

    def move(self, speed):
        self.cactus_rect.centerx -= speed
        self.win.blit(self.random_cactus, self.cactus_rect)
        if self.cactus_rect.centerx <= 0:
            self.cactus_rect.centerx = self.x
            self.big_small()
        if self.cactus_rect.centerx <= 300:
            pass
            # self.random_cactus = random.choice(self.cactuses)
    

# Basic setup
pygame.init()
clock = pygame.time.Clock()

# Game Costants
HEIGHT = 600
WIDTH = 1100
# WIDTH = 2404//2
GAME_SPEED = 0.25


screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chrome-Dino")

a = 0
# Dino
moving_sprites = pygame.sprite.Group()
dino = Dino( 50,HEIGHT/2)
moving_sprites.add(dino)

# Base
base = Base(WIDTH, 355, screen)

# Cactus
cactus = Cactus(HEIGHT, screen, WIDTH)
cactus.big_small()
score = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if ((event.key == pygame.K_UP) or (event.key == pygame.K_SPACE) and(dino.IN_AIR == False)):
                dino.jump()
            if event.key == pygame.K_DOWN:
                dino.duck()
        

    
# Drawing
    # Background
    screen.fill((255,255,255))
    # Dino
    dino.run()
    moving_sprites.draw(screen)
    moving_sprites.update(GAME_SPEED)
    # Base
    base.move(GAME_SPEED*50)
    # Cactus
    cactus.move(GAME_SPEED*50)
    # Speed
    if GAME_SPEED != 0.7:
        GAME_SPEED += 0.1/500
    #score
    score += GAME_SPEED
    print(int(score))
    pygame.display.flip()
    clock.tick(30)
    
