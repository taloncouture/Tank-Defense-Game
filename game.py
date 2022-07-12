import pygame
import sys
import time
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, reload_time, num_lives):
        super().__init__()

        tank_1 = pygame.image.load("tank_ice_1.png")
        tank_1 = pygame.transform.scale(tank_1, (width, height))
        tank_2 = pygame.image.load("tank_ice_2.png")
        tank_2 = pygame.transform.scale(tank_2, (width, height))
        self.frames = [tank_1, tank_2]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.width = width
        self.height = height

        self.direction = 'right'

        self.reload_time = reload_time
        self.reload_status = 0

        self.num_lives = num_lives

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.collision()
        obstacle_collide(self)
        self.input()
        lives(45, 45, self.num_lives)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= speed
            self.animation_state()
            self.image = pygame.transform.rotate(self.image, 90)
            self.direction = 'left'

            if obstacle_collide(self):
                self.rect.x += speed

        elif keys[pygame.K_DOWN] and self.rect.y + self.height < screen_height:
            self.rect.y += speed
            self.animation_state()
            self.image = pygame.transform.rotate(self.image, 180)
            self.direction = 'down'

            if obstacle_collide(self):
                self.rect.y -= speed

        elif keys[pygame.K_RIGHT] and self.rect.x + self.width < screen_width:
            self.rect.x += speed
            self.animation_state()
            self.image = pygame.transform.rotate(self.image, -90)
            self.direction = 'right'

            if obstacle_collide(self):
                self.rect.x -= speed
 
        elif keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= speed
            self.animation_state()
            self.direction = 'up'

            if obstacle_collide(self):
                self.rect.y += speed

        if keys[pygame.K_SPACE] and int(self.reload_status) >= self.reload_time:
            bullet = Bullet(self.rect.x + self.width / 2, self.rect.y, 16, 16, (0, 0, 0), self.direction, bullet_speed)
            bullet_group.add(bullet)
            self.reload_status = 0
            pygame.mixer.Sound.play(shoot_sound)

        elif keys[pygame.K_SPACE] and int(self.reload_status) < self.reload_time:
            self.reload_status = 0

        self.reload_status += 0.1

        reload_bar(self.reload_status, self.reload_time, 100, 40, screen_width / 2 - 50, screen_height - 40)

    def collision(self):
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.num_lives -= 1
            if self.num_lives > 0:
                pygame.mixer.Sound.play(lost_life_sound)

            reset()

        if pygame.sprite.spritecollide(flag, enemy_group, False):
            self.num_lives -= 1
            if self.num_lives > 0:
                pygame.mixer.Sound.play(lost_life_sound)
            
            reset()
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, direction, speed):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.bullet_direction = direction
        self.speed = speed

        self.score = 0

        if self.bullet_direction == 'right':
            self.rect.x = int(x + width + speed * 2)
            self.rect.y = y + int(0.5 * tank_height) - int(0.5 * height)

        if self.bullet_direction == 'left':
            self.rect.x = int(x - width * 2 - speed * 2)
            self.rect.y = int(y + (0.5 * tank_height) - (0.5 * height))

        if self.bullet_direction == 'up':
            self.rect.x = int(x - (0.5 * width))
            self.rect.y = int(y - height - speed)

        if self.bullet_direction == 'down':
            self.rect.x = int(x - (0.5 * width))
            self.rect.y = int(y + tank_height + speed)

    def update(self):

        self.collision()

        if self.bullet_direction == 'right':
            self.rect.x += self.speed

        if self.bullet_direction == 'left':
            self.rect.x -= self.speed

        if self.bullet_direction == 'up':
            self.rect.y -= self.speed

        if self.bullet_direction == 'down':
            self.rect.y += self.speed

    def collision(self):
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()
            global player_score
            player_score += 1
            pygame.mixer.Sound.play(destroy_sound)

        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            player.num_lives -= 1
            if player.num_lives > 0:
                pygame.mixer.Sound.play(lost_life_sound)
            reset()

        if self.rect.x > screen_width or self.rect.y > screen_height or self.rect.x < 0 or self.rect.y < 0:
            self.kill()
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, type, shoot_delay, bullet_speed):
        super().__init__()

        self.speed = speed
        self.width = width
        self.height = height
        
        if type == 'car':
            enemy_1 = pygame.image.load("car_1.png")
            enemy_1 = pygame.transform.scale(enemy_1, (width, height))
            enemy_2 = pygame.image.load("car_2.png")
            enemy_2 = pygame.transform.scale(enemy_2, (width, height))
            self.frames = [enemy_1, enemy_2]
            self.animation_index = 0
            self.image = self.frames[self.animation_index]

        if type == 'tank':

            enemy_1 = pygame.image.load('enemy_1.png')
            enemy_1 = pygame.transform.scale(enemy_1, (width, height))
            enemy_2 = pygame.image.load('enemy_2.png')
            enemy_2 = pygame.transform.scale(enemy_2, (width, height))
            self.frames = [enemy_1, enemy_2]
            self.animation_index = 0
            self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shoot_index = 0
        self.shoot_delay = shoot_delay
        self.variation = type
        self.bullet_speed = bullet_speed

        self.direction = 'right'

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]


    def update(self):

        self.move()
        self.shoot_index += 0.1
        self.shoot()
      

    def move(self):
            if self.rect.x < screen_width / 2 + self.width / 2 and abs(self.rect.x - (screen_width / 2)) >= abs(self.rect.y - (screen_height / 2)) and obstacle_collide(self) == False:
                self.rect.x += self.speed
                self.animation_state()
                self.image = pygame.transform.rotate(self.image, -90)
                self.direction = 'right'

            if self.rect.x > screen_width / 2 - self.width / 2 and abs(self.rect.x - (screen_width / 2)) >= abs(self.rect.y - (screen_height / 2)) and obstacle_collide(self) == False:
                self.rect.x -= self.speed
                self.animation_state()
                self.image = pygame.transform.rotate(self.image, 90)
                self.direction = 'left'

            if self.rect.y > screen_height / 2 - self.height / 2 and abs(self.rect.x - (screen_width / 2)) < abs(self.rect.y - (screen_height / 2)) and obstacle_collide(self) == False:
                self.rect.y -= self.speed
                self.animation_state()
                self.direction = 'up' 

            if self.rect.y < screen_height / 2 + self.height / 2 and abs(self.rect.x - (screen_width / 2)) < abs(self.rect.y - (screen_height / 2)) and obstacle_collide(self) == False:
                self.rect.y += self.speed
                self.animation_state()
                self.image = pygame.transform.rotate(self.image, 180)
                self.direction = 'down'

    def shoot(self):
        if self.variation == 'tank':
            if self.shoot_index >= self.shoot_delay:
                bullet = Bullet(self.rect.x + self.width / 2, self.rect.y, 16, 16, (0, 0, 0), self.direction, self.bullet_speed)
                bullet_group.add(bullet)
                self.shoot_index = 0
        
class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.x = x
        self.y = y

        flag = pygame.image.load("flag.png")
        flag = pygame.transform.scale(flag, (self.width, self.height))
        self.image = flag
        self.rect = self.image.get_rect(center = (self.x, self.y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        obstacle = pygame.image.load("obstacle.png")
        obstacle = pygame.transform.scale(obstacle, (self.width, self.height))
        self.image = obstacle
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

def obstacle_collide(sprite):
    if pygame.sprite.spritecollide(sprite, flag_group, False):
        return True
    else:
        return False

def spawn_enemies(tank_chance, shoot_delay, enemy_speed, bullet_speed):
        
    sides = ['left', 'right', 'up', 'down']
    choice = random.choice(sides)

    enemy_type = random.randint(0, tank_chance)
    if enemy_type == tank_chance:
        enemy_type = 'tank'
        enemy_speed = int(enemy_speed / 2)
    else:
        enemy_type = 'car'

    if choice == 'left':
        enemy = Enemy(0 - tank_width, random.randint(0, screen_height - tank_height), tank_width, tank_height, enemy_speed, enemy_type, shoot_delay, bullet_speed)
        enemy_group.add(enemy)

    if choice == 'right':
        enemy = Enemy(screen_width, random.randint(0, screen_height - tank_height), tank_width, tank_height, enemy_speed, enemy_type, shoot_delay, bullet_speed)
        enemy_group.add(enemy)

    if choice == 'up':
        enemy = Enemy(random.randint(0, screen_width - tank_width), -tank_height, tank_width, tank_height, enemy_speed, enemy_type, shoot_delay, bullet_speed)
        enemy_group.add(enemy)

    if choice == 'down':
        enemy = Enemy(random.randint(0, screen_width - tank_width), screen_height, tank_width, tank_height, enemy_speed, enemy_type, shoot_delay, bullet_speed)
        enemy_group.add(enemy)

def reload_bar(reload_status, reload_time, width, height, x, y):
    reload_bar_1 = pygame.image.load("reload_bar_1.png")
    reload_bar_1 = pygame.transform.scale(reload_bar_1, (width, height))
    reload_bar_2 = pygame.image.load("reload_bar_2.png")
    reload_bar_2 = pygame.transform.scale(reload_bar_2, (width, height))
    reload_bar_3 = pygame.image.load("reload_bar_3.png")
    reload_bar_3 = pygame.transform.scale(reload_bar_3, (width, height))
    reload_bar_4 = pygame.image.load("reload_bar_4.png")
    reload_bar_4 = pygame.transform.scale(reload_bar_4, (width, height))
    reload_bar_frames = [reload_bar_1, reload_bar_2, reload_bar_3, reload_bar_4]

    i = reload_status / reload_time

    if i >= 0 and i <= 0.25:
        screen.blit(reload_bar_frames[0], (x, y))
    if i > 0.25 and i <= 0.5:
        screen.blit(reload_bar_frames[1], (x, y))
    if i > 0.5 and i <= 0.99:
        screen.blit(reload_bar_frames[2], (x, y))
    if i >= 1:
        screen.blit(reload_bar_frames[3], (x, y)) 

def lives(width, height, num_lives):
    margin = 20

    icon = pygame.image.load("tank_icon_ice.png")
    icon = pygame.transform.scale(icon, (width, height))

    if num_lives == 3:
        screen.blit(icon, (margin, margin / 2))
        screen.blit(icon, (margin + width + margin, margin / 2))
        screen.blit(icon, (margin + width + margin + width + margin, margin / 2))
    if num_lives == 2:
        screen.blit(icon, (margin, margin / 2))
        screen.blit(icon, (margin + width + margin, margin / 2))
    if num_lives == 1:
        screen.blit(icon, (margin, margin / 2))

def reset():
    for enemy in enemy_group:
        enemy.kill()

    player.rect.x = screen_width / 2 - player.width / 2
    player.rect.y = screen_width / 2 - player.height / 2 + flag_height

def score():
    margin = 20

    score_text = score_font.render(str(player_score), False, (255, 255, 255))
    score_text_rect = score_text.get_rect(topright = (screen_width - margin, margin))
    screen.blit(score_text, score_text_rect)

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Defense")
game_active = False

background = pygame.image.load("ground.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

game_font = pygame.font.Font('8bitOperatorPlus8-Regular.ttf', 30)
small_game_font = pygame.font.Font('8bitOperatorPlus8-Bold.ttf', 15)
title_font = pygame.font.Font('8bitOperatorPlus8-Bold.ttf', 60)
score_font = pygame.font.Font('8bitOperatorPlus8-Regular.ttf', 40)

shoot_sound = pygame.mixer.Sound('tank_shoot.wav')
destroy_sound = pygame.mixer.Sound('hit.wav')
lost_life_sound = pygame.mixer.Sound('lost_life.wav')
click_sound = pygame.mixer.Sound('click.wav')
game_over_sound = pygame.mixer.Sound('game_over2.wav')

tank_x = 0
tank_y = 0

tank_height = 64
tank_width = 64

flag_width = 80
flag_height = 80

obstacle_width = 80
obstacle_height = 80

tile_width = 80
tile_height = 80

speed = 7
bullet_speed = 16

reload_time = 2

difficulty_modifier = 0.05
spawn_time = 6
spawn_status = 0

player_score = 0

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
flag_group = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()

while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_active == False:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(click_sound)
                    game_active = True
                    player_score = 0

                    player = Player(screen_width / 2 - tank_width / 2, screen_height / 2 - tank_height / 2 + flag_height, tank_width, tank_height, speed, 2, 3)
                    player_group.add(player)

                    flag = Flag(screen_width / 2, screen_height / 2, flag_width, flag_height)
                    flag_group.add(flag)


        if game_active:
            
            screen.blit(background, (0, 0))
            player_group.draw(screen)
            enemy_group.draw(screen)
            flag_group.draw(screen)
            obstacle_group.draw(screen)
            bullet_group.draw(screen)
            player_group.update()
            bullet_group.update()
            enemy_group.update()
            flag_group.update()
            difficulty_modifier += 0.000001
            score()

            if (player.num_lives <= 0):
                pygame.mixer.Sound.play(game_over_sound)
                game_active = False

                for bullet in bullet_group:
                    bullet.kill()
                for enemy in enemy_group:
                    enemy.kill()
                for player in player_group:
                    player.kill()

            if spawn_status >= spawn_time:
                spawn_enemies(3, 9, 2, 8)
                spawn_status = 0
            else:
                spawn_status += difficulty_modifier

        else:
            if player_score == 0:
                screen.fill((20, 120, 20))
                title_message = title_font.render('Tank Defense', False, (255, 255, 255))
                title_message_rect = title_message.get_rect(center = (screen_width / 2, screen_height / 2))
                screen.blit(title_message, title_message_rect)
                play_message = game_font.render("Press Space to Start", False, (255, 255, 255))
                play_message_rect = play_message.get_rect(center = (screen_width / 2, screen_height / 2 + screen_height / 6))
                screen.blit(play_message, play_message_rect)
                credits_message = small_game_font.render("Created by Talon Couture", False, (255, 255, 255))
                credits_message_rect = credits_message.get_rect(midbottom = (screen_width / 2, screen_height - 5))
                screen.blit(credits_message, credits_message_rect)
            else:
                screen.fill((20, 120, 20))
                title_message = title_font.render('Game Over', False, (255, 255, 255))
                title_message_rect = title_message.get_rect(center = (screen_width / 2, screen_height / 2 - screen_height / 8))
                screen.blit(title_message, title_message_rect)
                score_message = game_font.render(f"Your Score: {player_score}", False, (255, 255, 255))
                score_message_rect = score_message.get_rect(center = (screen_width / 2, screen_height / 2))
                screen.blit(score_message, score_message_rect)
                play_message = game_font.render("Press Space to Start", False, (255, 255, 255))
                play_message_rect = play_message.get_rect(center = (screen_width / 2, screen_height / 2 + screen_height / 8))
                screen.blit(play_message, play_message_rect)
                credits_message = small_game_font.render("Created by Talon Couture", False, (255, 255, 255))
                credits_message_rect = credits_message.get_rect(midbottom = (screen_width / 2, screen_height - 5))
                screen.blit(credits_message, credits_message_rect)

        pygame.display.update()
        clock.tick(60)