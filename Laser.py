import pygame
from pygame import mixer
from sys import exit
from random import randint, choice
from pygame.constants import K_s

mixer.init()
pygame.init()

# Create the window
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Defenders Of The Universe')
earth = pygame.image.load('Data/BONUS/Earth.png')
earth = pygame.transform.scale(earth, (int(earth.get_width() * 0.5), (int(earth.get_height() * 0.5))))
pygame.display.set_icon(earth)

# Set FPS
clock = pygame.time.Clock()

# Game variables
start_time = 0
dead = False
test_font = pygame.font.Font('Data/font/Pixeltype.ttf', 25)
begining_font = pygame.font.Font('Data/font/Pixeltype.ttf', 25)
score = 0
game_active = False
HEALTH = 100
shoot = False

# Game Musix and SFX
shot_fx = pygame.mixer.Sound('Data/BONUS/laser.wav')
shot_fx.set_volume(0.2)

at_music = pygame.mixer.Sound('Data/BONUS/AttackTheme.wav')
at_music.play(loops = -1)
at_music.set_volume(0.3)

# Load images
# Background
sky_surface = pygame.image.load('Data/Backgrounds/test.png').convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_surface = pygame.image.load('Data/Backgrounds/testPlayer.png').convert_alpha()
        self.image = player_surface 
        self.rect = self.image.get_rect(midbottom = (200, 600))
    def update(self):
        self.shoot()

    def shoot(self):
        if shoot:
            pygame.draw.line(screen, 'Red', (200, 500), pygame.mouse.get_pos(), 8)
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        self.fx_death = pygame.mixer.Sound('Data/BONUS/explosion3.wav')
        self.fx_death.set_volume(0.2)
        
        if type == 'enemy1':
            enemy_1 = pygame.image.load('Data/PNG/Enemies/enemyBlack1.png').convert_alpha()
            enemy_1 = pygame.transform.scale(enemy_1, (int(enemy_1.get_width() * 0.5), (int(enemy_1.get_height() * 0.5))))
            self.frames = [enemy_1]
            y_pos = -1
        elif type == 'enemy2':
            enemy_2 = pygame.image.load('Data/PNG/Enemies/enemyGreen2.png').convert_alpha()
            enemy_2 = pygame.transform.scale(enemy_2, (int(enemy_2.get_width() * 0.5), (int(enemy_2.get_height() * 0.5))))
            self.frames = [enemy_2]
            y_pos  = -1
        else:
            enemy_3 = pygame.image.load('Data/PNG/Enemies/enemyBlue4.png').convert_alpha()
            enemy_3 = pygame.transform.scale(enemy_3, (int(enemy_3.get_width() * 0.5), (int(enemy_3.get_height() * 0.5))))
            self.frames = [enemy_3]
            y_pos  = -1
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(10,390),y_pos))

    def animation_state(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.y += 3.5
        self.destroy()

    def destroy(self):
        if self.rect.y >= 480:
            self.fx_death.play()
            self.kill()
            
    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            self.fx_death.play()
            self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,('White'))
	score_rect = score_surf.get_rect(center = (200,50))
	screen.blit(score_surf,score_rect)
	return current_time

# Set the game_active to true or false depending if player and enemy ship has collided
def check_alive():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1530)
obstacle2_timer = pygame.USEREVENT + 4
pygame.time.set_timer(obstacle2_timer,900)
# Intro Screen
game_name = begining_font.render('Defenders of the Universe',True,(111,196,169))
game_name_rect = game_name.get_rect(center =(200,80))

game_how = begining_font.render('How To Play: Click on the Ships', True, 'White') 
game_how1 = begining_font.render('to stay alive for as long as possible.', True, ('White'))
game_how2 = game_how
game_how3 = game_how1
game_how_rect = game_how2.get_rect(center = (200, 400))
game_how_rect1 = game_how3.get_rect(center = (200, 450))
game_message = begining_font.render('Press space to Start',True,(111,196,169))
game_message_rect = game_message.get_rect(center = (200,330))

# GAME LOOP
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_s:
                at_music.stop()
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot = True
            shot_fx.play()
            for object in obstacle_group:
                object.check_click(event.pos)
            
        if event.type == pygame.MOUSEBUTTONUP:
            shoot = False
            

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['enemy1','enemy2','enemy3'])))
            if event.type == obstacle2_timer:
                obstacle_group.add(Obstacle(choice(['enemy1','enemy2','enemy3'])))
		
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        
        screen.blit(sky_surface,(0,0))
        
        score = display_score()

        player.draw(screen)
        player.update()
        

        obstacle_group.draw(screen)
        obstacle_group.update()
       
        game_active = check_alive() 
        
    else:
        
        screen.blit(sky_surface, (0,0))
        screen.blit(earth, (100, 100))
        score_message = begining_font.render(f'Your score: {score}',True,(111,196,169))
        score_message_rect = score_message.get_rect(center = (200,330))
        screen.blit(game_name,game_name_rect)

        if score == 0: 
            screen.blit(game_message,game_message_rect) 
            screen.blit(game_how2, game_how_rect)
            screen.blit(game_how3, game_how_rect1)
        else: screen.blit(score_message,score_message_rect)
    
    pygame.display.update()
    clock.tick(60)