import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT= 400,800
HEALTH = 100
VELOCITY = 2
PROJECTILE_VELOCITY = 4
FPS = 60
WHITE = (0,0,0)
BLACK = (0,0,0)

player_lives = 3
bonus_score = 0

pygame.font.init()
score_font = pygame.font.Font(None, 50)
final_font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Shooty Game")

levels = {0:0, 1:50, 2:50, 3:50, 4:1, 5:0} #Level construct in dict form
enemy_health_levels = {0:0, 1:10, 2:20, 3:30, 4:250}

class Player(pygame.sprite.Sprite):     #Player class
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/Self.png').convert_alpha(), (50,50))
        self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH / 2,SCREEN_HEIGHT - 100))
        self.width = 50
        self.height = 30
        self.bullet_level = 1
        self.length_of_time = 0

    def update(self):                   #Continuously monitor inputs
        self.player_input()
        self.length_of_time += int(pygame.time.get_ticks() / 5000)

    def game_length_of_time(self):
        return self.length_of_time

    def draw_health(self, surf):        #Player health bar drawing
        health_rect = pygame.Rect(0, 0, 10, 5)
        health_rect.midbottom = self.rect.centerx -35, self.rect.top -5
        max_health = 10
        draw_health_bar(surf, health_rect.topleft, health_rect.size, (0, 0, 0), (255, 0, 0), (0, 255, 0), player_health/max_health)

    def player_input(self):             #Inputs to move the player and shoot
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y - VELOCITY > 0:
            self.rect.y -= VELOCITY
        if keys[pygame.K_DOWN] and self.rect.y + VELOCITY + self.height < SCREEN_HEIGHT:
            self.rect.y += VELOCITY
        if keys[pygame.K_LEFT] and self.rect.x + VELOCITY > 0: 
            self.rect.x -= VELOCITY
        if keys[pygame.K_RIGHT] and self.rect.x + VELOCITY + self.width < SCREEN_WIDTH:
            self.rect.x += VELOCITY
        if keys[pygame.K_SPACE]:
            if self.bullet_level == 1:
                bullet = Projectile(self.rect.x + 25, self.rect.y,1,1)
                projectiles.add(bullet)
                all_sprites.add(bullet)
            if self.bullet_level == 2:
                for i in range(3):
                    bullet = Projectile(self.rect.x + 25, self.rect.y,1,i+1)
                    projectiles.add(bullet)
                    all_sprites.add(bullet)
            if self.bullet_level == 3:
                for i in range(5):
                    bullet = Projectile(self.rect.x + 25, self.rect.y,1,i+1)
                    projectiles.add(bullet)
                    all_sprites.add(bullet)
                
class Enemy(pygame.sprite.Sprite):      #Enemy Class
    def __init__(self, enemy_level, enemy_health):
        super().__init__()
        self.enemy_level = enemy_level
        self.enemy_health = enemy_health
        self.image = pygame.transform.scale(pygame.image.load('Images/Enemy' + str(self.enemy_level) + '.png').convert_alpha(), (30,30))
        self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH - 10, 100))
        self.velocity = VELOCITY/2

    def update(self):                       #Move enemies in pattern
        enemy_position_y = int(self.rect.y/100) % 2
        if enemy_position_y == 1 and self.rect.x > 50:
            self.move_left()
        elif enemy_position_y == 0 and self.rect.x < 350:
            self.move_right()
        else:
            self.move_down()
        self.check_collision_bullet_enemy() #call for check for killing enemies
        if self.rect.y > SCREEN_HEIGHT:
            enemy = Enemy(current_level_index,enemy_health_levels[current_level_index])
            all_sprites.add(enemy)
            enemies.add(enemy)
            self.kill()

    def move_left(self):                    #Move enemy left
        self.rect.x -= self.velocity

    def move_right(self):                   #Move enemy right
        self.rect.x += self.velocity

    def move_down(self):                    #Move enemy down
        self.rect.y += self.velocity

    def check_collision_bullet_enemy(self): #check for bullet to enemy collision
        if pygame.sprite.spritecollide(self, projectiles, False):
            self.enemy_health -= 1
            update_enemy_kills(1)
            if self.enemy_health < 0:
                self.kill()
            return False
        else: return True

class Projectile(pygame.sprite.Sprite):     #Projectile class
    def __init__(self,loc_x,loc_y,shoot_level, shoot_type):
        super().__init__()
        self.vel = PROJECTILE_VELOCITY
        self.image = pygame.transform.scale(pygame.image.load('Images/Bullet-blue.png').convert_alpha(), (5,5))
        self.rect = self.image.get_rect(center = (loc_x, loc_y))
        self.shoot_level = shoot_level
        self.shoot_type = shoot_type
    
    def update(self):                       #call for move bullets and self kill once bullets move off screen
        self.projectile_move()
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

    def projectile_move(self):              #Movement of bullets after firing
        if self.shoot_type == 1:
            self.rect.y -= self.vel
        if self.shoot_type == 2:
            self.rect.y -= self.vel
            self.rect.x -= self.vel
        if self.shoot_type == 3:
            self.rect.y -= self.vel
            self.rect.x += self.vel
        if self.shoot_type == 4:
            self.rect.x -= self.vel
        if self.shoot_type == 5:
            self.rect.x += self.vel
             
class Powerups(pygame.sprite.Sprite):       #Class for powerups
    def __init__(self):
        super().__init__()
        self.type = random.choice(['gun','health','score'])
        if self.type == 'gun':
            self.image = pygame.transform.scale(pygame.image.load('Images/gun.png').convert_alpha(), (30,30))
        elif self.type == 'health':
            self.image = pygame.transform.scale(pygame.image.load('Images/health.png').convert_alpha(), (30,30))
        elif self.type == 'score':
            self.image = pygame.transform.scale(pygame.image.load('Images/score.png').convert_alpha(), (50,30))
        self.rect = self.image.get_rect(center = (random.random() * SCREEN_WIDTH, 0))
        self.vel = VELOCITY / 2

    def update(self):                       #call for movement on screen and self kill
        self.rect.y += self.vel
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        
def display_lives(current_lives):           #Display current lives on screen
    player_lives_surf = final_font.render(f'Remaining lives: {current_lives}',False,(64,64,64))
    player_lives_rect = player_lives_surf.get_rect(center = (300,20))
    screen.blit(player_lives_surf,player_lives_rect)

def display_level(current_level):           #Display current level on screen
    current_level_surf = final_font.render(f'Level: {current_level}',False,(64,64,64))
    current_level_rect = current_level_surf.get_rect(center = (40,20))
    screen.blit(current_level_surf,current_level_rect)

def update_enemy_kills(enemy_killed):       #Track enemies killed
    global enemy_kills
    enemy_kills += enemy_killed

def display_score():                        #Display score on screen
	score_surf = score_font.render(f'Score: {player.game_length_of_time() + (enemy_kills *10) + bonus_score}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (200,50))
	screen.blit(score_surf,score_rect)

def start_screen():                         #Start Screen Format
    start_screen_surf = final_font.render(f'Press 1 to start Game',False,(64,64,64))
    start_screen_rect = start_screen_surf.get_rect(center = (200,200))
    screen.blit(start_screen_surf,start_screen_rect)
    pygame.display.update()

def draw_health_bar(surf, pos, size, borderC, backC, healthC, progress):        #Draw health bar
    pygame.draw.rect(surf, backC, (*pos, *size))
    pygame.draw.rect(surf, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+1, pos[1]+1)
    innerSize = ((size[0]-2) * progress, size[1]-2)
    rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
    pygame.draw.rect(surf, healthC, rect)

all_sprites = pygame.sprite.Group()     #add all sprites to Groups
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()

running = True 
clock = pygame.time.Clock()
Background_Y = 0
score = 0
game_active = False
start_screen()
current_level_index = 1
Background = pygame.transform.scale(pygame.image.load('Images/Turf.jpg').convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))

while running:                          #Game loop
    for event in pygame.event.get():    #Check for quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:    #Check for game start
            pygame.sprite.Group.empty(all_sprites)
            pygame.sprite.Group.empty(enemies)
            pygame.sprite.Group.empty(projectiles)
            pygame.sprite.Group.empty(obstacles)                
            pygame.sprite.Group.empty(powerups)

            player_health = 100     #Reset Particulars on start
            enemy_kills = 0
            game_active = True
            enemies_deployed = levels[current_level_index]
            player = Player()
            all_sprites.add(player)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:    #Check for game start
            pygame.sprite.Group.empty(all_sprites)
            pygame.sprite.Group.empty(enemies)
            pygame.sprite.Group.empty(projectiles)
            pygame.sprite.Group.empty(obstacles)
            pygame.sprite.Group.empty(powerups)

            player_lives = 3
            player_health = 100     #Reset Particulars on start
            enemy_kills = 0
            game_active = True
            current_level_index = 0
            enemies_deployed = levels[current_level_index]
            player = Player()
            all_sprites.add(player)
            score = 0

    if game_active:        
        for i in range(3):              #Moving Background
            screen.blit(Background, (0, i * -SCREEN_HEIGHT + Background_Y))
        Background_Y += 1
        if Background_Y > SCREEN_HEIGHT:
            Background_Y = 0
        
        if enemies_deployed != 0:       #Deploy enemies
            if random.random() > 0.9:
                enemy = Enemy(current_level_index,enemy_health_levels[current_level_index])
                all_sprites.add(enemy)
                enemies.add(enemy)
                enemies_deployed -= 1

        if enemies_deployed <= 0 and len(enemies.sprites()) == 0 and current_level_index < 5:               #Increase level
            current_level_index += 1 
            enemies_deployed = levels[current_level_index]
		
        if random.random() > 0.995:     #Deploy powerups
            powerup = Powerups()
            all_sprites.add(powerup)
            powerups.add(powerup)

        all_sprites.update()            #Display items on screen
        score = display_score()
        player.draw_health(screen)
        display_lives(player_lives)	
        display_level(current_level_index)	

        hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)    #Powerup upgrades
        for hit in hits:
            if hit.type == 'gun':
                player.bullet_level += 1
                if player.bullet_level == 3:
                    player.bullet_level = 3
            if hit.type == 'health' and player_health < 80:
                player_health += 50
            if hit.type == 'score':
                bonus_score += 1000

        if pygame.sprite.spritecollideany(player,enemies) != None:      #Enemy collision
            player_health -= 1
            
        if player_health < 0 and player_lives > 0:      #Lost Life
            player_lives -= 1
            screen.fill(BLACK)
            display_lives(player_lives)	
            final_message = final_font.render(f'You have been killed!',False,(64,64,64))
            final_rect = final_message.get_rect(center = (200,400))
            screen.blit(final_message,final_rect)
            restart_message = final_font.render(f'Press 1 to restart.',False,(64,64,64))
            restart_rect = restart_message.get_rect(center = (200,500))
            screen.blit(restart_message,restart_rect)
            game_active = False
            pygame.display.update()

        elif player_lives <= 0 :        #Game Over from dieing
                final_message = final_font.render(f'You have been killed! and no lives left',False,(64,64,64))
                final_rect = final_message.get_rect(center = (200,400))
                screen.blit(final_message,final_rect)
                restart_message = final_font.render(f'Press Enter to restart game',False,(64,64,64))
                restart_rect = restart_message.get_rect(center = (200,500))
                screen.blit(restart_message,restart_rect)
                score = display_score()
                pygame.display.update()
                game_active = False
                
        elif current_level_index == 5: #Game finished
                final_message = final_font.render(f'You have killed the boss!',False,(64,64,64))
                final_rect = final_message.get_rect(center = (200,400))
                screen.blit(final_message,final_rect)
                restart_message = final_font.render(f'Press Enter to restart game',False,(64,64,64))
                restart_rect = restart_message.get_rect(center = (200,500))
                screen.blit(restart_message,restart_rect)
                score = display_score()
                pygame.display.update()
                game_active = False
                
        all_sprites.draw(screen)    #Update screen
        pygame.display.update()
        clock.tick(FPS)
        
pygame.quit()       #Quit
sys.exit()
