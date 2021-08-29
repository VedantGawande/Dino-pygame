# Special thanks to Klass and Lalit
# Importing
import pygame
from sys import exit
from random import choice, randint

# ----Player class----
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Loading jumping audio and all of the sprites
        self.jump_audio = pygame.mixer.Sound('Assets/Audio/Jump.mp3')
        self.dino_1 = pygame.image.load('Assets/Dino/DinoRun1.png').convert_alpha()
        self.dino_2 = pygame.image.load('Assets/Dino/DinoRun2.png').convert_alpha()
        self.dino_jump = pygame.image.load('Assets/Dino/DinoJump.png').convert_alpha()
        self.dino_duck_1 = pygame.image.load('Assets/Dino/DinoDuck1.png').convert_alpha()
        self.dino_duck_2 = pygame.image.load('Assets/Dino/DinoDuck2.png').convert_alpha()
        self.dino_dead =  pygame.image.load('Assets/Dino/DinoDead.png').convert_alpha()

        self.gravity = 0 # default player gravity
        self.index = 0 # default player animation index
        self.dino = [self.dino_1, self.dino_2, self.dino_duck_1, self.dino_duck_2] # adding all the sprites in a list
        self.image = self.dino[self.index] # image which will be displayed
        self.rect = self.image.get_rect(bottomleft=(60,370)) # rect of the image
    
    def jump(self):
        # If space or up key is pressed and the player is on the ground and down key is not pressed(since, we force the player to get down if it is press) the player will jump
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 370 and keys[pygame.K_DOWN] == False:
            self.jump_audio.play()
            self.gravity = -20

    def duck(self):
        # If down key is pressed in mid-air gravity will increase, forcing the player get down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]: self.gravity = 20

    def apply_gravity(self): # Appling gravity
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 370: self.rect.bottom = 370 # So that player wont go below the ground(since ground is placed at y=350)

    def anim(self): # Animating the player
        if self.rect.bottom < 370: self.image = self.dino_jump
        else:
            self.index += game_speed/60

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.rect.y += 94

                if self.index <= 1 or self.index >= 4: self.index = 2 
                
            else:
                if self.index >= 2: self.index = 0
            self.image = self.dino[int(self.index)]
            self.rect = self.image.get_rect(bottomleft=(60,370))
    
    def update(self): # Updating the player
        self.anim()
        self.apply_gravity()
        self.jump()
        self.duck()

# ----Ground class----
class Ground:
    def __init__(self):
        self.image = pygame.image.load('Assets/Other/Track.png').convert_alpha() # Loading ground image
        self.x_pos = 0
        self.image_width = 2404 # width of track.png
        self.rect = self.image.get_rect(topleft=(self.x_pos, 350))
        self.rect2 = self.image.get_rect(topleft=(self.x_pos+self.image_width, 350))
    
    def move(self): # moving the ground to left
        if self.x_pos+self.image_width <= 0: self.x_pos = 0
        self.x_pos -= game_speed # so that movement of the cloud is infuenced by the game speed
        self.rect = self.image.get_rect(topleft=(self.x_pos, 350))
        self.rect2 = self.image.get_rect(topleft=(self.x_pos+self.image_width, 350))
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect2)
    
    def update(self):
        self.move()

# ----Clouds class----
class Cloud(pygame.sprite.Sprite):
    '''
    Logic --> Generate a random y position --> make the cloud move slower than other things to left-->destroy the cloud if it is out of the screen
    '''
    def __init__(self):
        super().__init__()
        self.x = 1700
        self.y = randint(50,250) # so that every cloud's height is different
        self.image = pygame.image.load('Assets/Other/Cloud.png') # loading image of cloud
        self.rect = self.image.get_rect(topright=(self.x, self.y))
    
    def move(self):
        self.x -= int(game_speed/4)
        self.rect = self.image.get_rect(topright=(self.x, self.y))
    
    def destroy(self): # if the cloud is out of the screen it will get destroyed
        if self.x <= -100: self.kill()

    def update(self):
        self.move()
        self.destroy()

# ----Obstacle class----
class Obstacle(pygame.sprite.Sprite):
    '''
    Logic --> type --> if cactus --> random sprite/cactus type --> random spawn after 3 sec--> destroy cactus after it's out of screen
                   --> if bird --> animate --> random spawn after 3 sec --> destroy cactus after it's out of screen
    '''
    def __init__(self, type):
        super().__init__()
        global game_speed
        self.index = 0
        self.obstacle = []
        self.type = type
        if self.type == 'cactus':
            self.index = randint(0,11)
            self.large_cactus1 = pygame.image.load('Assets/Cactus/LargeCactus1.png').convert_alpha()
            self.large_cactus2 = pygame.image.load('Assets/Cactus/LargeCactus2.png').convert_alpha()
            self.large_cactus3 = pygame.image.load('Assets/Cactus/LargeCactus3.png').convert_alpha()
            self.small_cactus1 = pygame.image.load('Assets/Cactus/SmallCactus1.png').convert_alpha()
            self.small_cactus2 = pygame.image.load('Assets/Cactus/SmallCactus2.png').convert_alpha()
            self.small_cactus3 = pygame.image.load('Assets/Cactus/SmallCactus3.png').convert_alpha()
            for i in range(3): #This is done 3 times as we need more possibility of single cactus
                self.obstacle.append(self.large_cactus1)
                self.obstacle.append(self.small_cactus1)
            for i in range(2):
                self.obstacle.append(self.large_cactus2)
                self.obstacle.append(self.small_cactus2)
            self.obstacle.append(self.large_cactus3)
            self.obstacle.append(self.small_cactus3)
             
            self.image = self.obstacle[self.index]
            self.rect = self.image.get_rect(bottomleft=(1200,370))
        else:
            self.bird_1 = pygame.image.load('Assets/Bird/Bird1.png').convert_alpha()
            self.bird_2 = pygame.image.load('Assets/Bird/Bird2.png').convert_alpha()
            self.obstacle = [self.bird_1, self.bird_2]
            self.image = self.obstacle[self.index]
            self.rect = self.image.get_rect(bottomleft=(1200,choice([350, 310, 270]))) # different hights so that the player could either jump, duck or stay as it is
    def move(self):
        self.rect.x -= game_speed
        if self.type == 'bird': self.rect.x -= 1 # so that bird moves faster than cactus
    
    def anim(self):
        if self.type == 'bird':
            self.index += 0.1
            if self.index >= len(self.obstacle): self.index = 0
            self.image = self.obstacle[int(self.index)]
            
    def destroy(self):
        if self.rect.x <= -120:
            self.kill()

    def update(self):
        self.destroy()
        self.move()
        self.anim()

# Checking collison
def collision():
    all_obstacles = obstacle.sprites()
    try:
        if pygame.sprite.collide_mask(player.sprite, all_obstacles[0]):
        # if pygame.sprite.spritecollide(player.sprite, obstacle, False):
            death_audio.play()
            player.sprite.image = dino_dead
            
            obstacle.empty()
            return False
    except:
        return True 
    return True

# Updatating game speed
def update_speed():
    global game_speed, obstacle_spawn_delay, score, start_time, can_speed
    score = int((pygame.time.get_ticks()-start_time)/1000*game_speed)
    if score % 100 == 0 and score != 0:
        if game_speed != 12: # max speed limit
            if can_speed:
                game_speed += 1
                can_speed = False
            # if obstacle_spawn_delay > 500:
            #     obstacle_spawn_delay -= 500
            else: obstacle_spawn_delay = 100
        # print(game_speed)
        # print(obstacle_spawn_delay)
    else:
        can_speed = True

# Updating High score
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        # Writing new high score in the file "high_score.txt"
        with open('high_score.txt', 'w+') as o:
            o.write(str(high_score))
            o.close()

# Playing sound if player gets to score which is multiple of 100 i.e 100, 200, 300 etc.
def play_sound_score():
    global play_sound
    if score % 100 == 0 and score != 0:
        if play_sound:
            score_audio.play()
            play_sound = False
    else:
        play_sound = True

# Initializing
pygame.init()
screen_width = 1100
screen_height = 420
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
run = False
play_sound = True
can_speed = True
score = 0
start_time = 0

# Font
font = pygame.font.Font('Assets/Font/Press Start 2P.ttf', 20)
font2 = pygame.font.Font('Assets/Font/Press Start 2P.ttf', 30)
game_speed = 10 # default speed

# Audio
death_audio = pygame.mixer.Sound('Assets/Audio/Death.mp3')
score_audio = pygame.mixer.Sound('Assets/Audio/Score.mp3')

# Dead image
dino_dead = pygame.image.load('Assets/Dino/DinoDead.png').convert_alpha()
dino_start = pygame.image.load('Assets/Dino/DinoStart.png').convert_alpha()

# Reset image
reset_image = pygame.image.load('Assets/Other/Reset.png').convert_alpha()

# Base/Ground
ground = Ground()

# Obstacle spawn timer
obstacle_timer = 500
# obstacle_spawn_delay = 1000
# pygame.time.set_timer(obstacle_timer, obstacle_spawn_delay)

# Cloud spawn timer
cloud_timer = pygame.USEREVENT + 1
cloud_spawn_delay = 4000
pygame.time.set_timer(cloud_timer, cloud_spawn_delay)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

cloud = pygame.sprite.Group()

obstacle = pygame.sprite.Group()


# Checking if there is a high score/ Loading high score
with open('high_score.txt', 'w+') as o:
    high_score = o.read()
    if high_score == '': high_score = 0
    else: high_score = int(high_score)
    o.close()
    
# ----Main loop----
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if run:
            # if event.type == obstacle_timer:
            #     obstacle.add(Obstacle(choice(['cactus', 'cactus', 'cactus', 'bird']))) # Scince bird spawning possibility should be less
            if event.type == cloud_timer:
                cloud.add(Cloud())
        else:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                run = True
                start_time = pygame.time.get_ticks()
    if run:
        if obstacle_timer > 0:
            obstacle_timer -= game_speed
        else:
            obstacle_timer = 500
            obstacle.add(Obstacle(choice(['cactus', 'cactus', 'cactus', 'bird'])))
        
        screen.fill((255,255,255))

        update_speed()         
        play_sound_score()

        # Displaying Score
        no_of_zero = (5-len(str(score)))*'0'
        score_message = font.render(f'{no_of_zero}{score}', False, (83,83,83))
        screen.blit(score_message, (screen_width-score_message.get_width()-10, 10))
        
        # Displaying High Score
        no_of_zero_high = (5-len(str(high_score)))*'0'
        high_score_message = font.render(f'HI {no_of_zero_high}{high_score}', False, (117,117,117))
        screen.blit(high_score_message, (screen_width-(score_message.get_width()*2)-110, 10))

        # Updating and drawing
        cloud.draw(screen)
        cloud.update()

        obstacle.draw(screen)
        obstacle.update()

        ground.update()
        player.update()
        run = collision()
        player.draw(screen)
        
        # Checking collison
        
    
    elif run != True and score == 0: # This means that the game is just launched
        screen.fill((255,255,255))
        screen.blit(dino_start, (50, 275))
        # Displaying instruction
        instruction = font2.render('PRESS SPACE TO START', False, (83,83,83))
        instruction_rect = instruction.get_rect(center=(screen_width/2, screen_height/2-50))
        screen.blit(instruction, instruction_rect)

    else: # This means that player has collided
        update_high_score()
        # player.draw(screen)
        player.sprite.rect.bottom = 370 # so that player will start from the ground
        game_speed = 10 # making it back to its original value
        # Displaying Death meesage
        screen.blit(reset_image, (screen_width/2-50, screen_height/2))
        death_message = font2.render('G A M E  O V E R', False, (83,83,83))
        death_message_rect = death_message.get_rect(center=(screen_width/2, screen_height/2-50))
        screen.blit(death_message, death_message_rect)

    pygame.display.update()
    clock.tick(60)
