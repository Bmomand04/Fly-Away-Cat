import pygame
import os
import random
import pygame.freetype

#-----------------------------VARIABLES, ASSETS, AND SET UP-------------------------------------------------
pygame.font.init()
pygame.mixer.init()
pygame.freetype.init()

# screen size
WIDTH, HEIGHT = 1920, 1020

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# title
pygame.display.set_caption("GAME")

# fps
FPS = 60

# velocity / movement
VEL = 10

# collision sound effect
damage_sfx = pygame.mixer.Sound("damage_sound.wav")

#point sound effect
point_sfx = pygame.mixer.Sound("point_sound.mp3")

# screen color / sky
SKY = (100, 255, 255)
GRASS_GREEN = (34, 177, 76)  # grass color

# player dimensions
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 150

# enemy dimensions
ENEMY_HEIGHT = 60
ENEMY_WIDTH = 70

#point dimensions
POINT_HEIGHT = 60
POINT_WIDTH = 70

# jumping
jumping = False
jumpVel = 10

# for facing left
facing_left = False

# text font
HEALTH_FONT = pygame.font.Font("PixelifySans.ttf", 40)
MAIN_MENU_FONT = pygame.font.Font("PixelifySans.ttf", 50)
SCORE_FONT = pygame.font.Font("PixelifySans.ttf", 40)

# invincibility after collide so health doesn't drop
timer_interval = 450 # 0.4 seconds
#score_timer_interval = 450
timer_event_id = pygame.USEREVENT + 1

#global player_health
#global score

#background music
pygame.mixer.music.load("bg_music.mp3")

# player image facing right
player_image_right_path = pygame.image.load(os.path.join('PixelCat_right.png'))  # loading from path
player_image_right = pygame.transform.scale(player_image_right_path, (PLAYER_WIDTH, PLAYER_HEIGHT))

# player image facing left
player_image_left_path = pygame.image.load(os.path.join('PixelCat_left.png'))
player_image_left = pygame.transform.scale(player_image_left_path, (PLAYER_WIDTH, PLAYER_HEIGHT))

# background
background_path = pygame.image.load(os.path.join('Background.png')).convert()
BG = pygame.transform.scale(background_path, (WIDTH, HEIGHT))

# enemy star
neon_enemy_path = pygame.image.load(os.path.join('neon_enemy.png'))
neon_enemy = pygame.transform.scale(neon_enemy_path, (ENEMY_WIDTH, ENEMY_HEIGHT))

#point star
point_star_path = pygame.image.load(os.path.join('point_star.png'))
point_star = pygame.transform.scale(point_star_path, (POINT_WIDTH, POINT_HEIGHT))

#damage taken cat
player_dmg_image_path = pygame.image.load(os.path.join('PixelCat_right_damage.png'))
player_dmg_image = pygame.transform.scale(player_dmg_image_path, (PLAYER_WIDTH, PLAYER_HEIGHT))

# ---------------------------------------------CLASSES AND GAME FUNCTIONS-----------------------------------------------------------------

class Enemy:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(0, HEIGHT - PLAYER_HEIGHT)
        self.vel = random.randint(5, 10)

    def move(self):
        self.x -= self.vel

    def draw(self):
        WIN.blit(neon_enemy, (self.x, self.y))

class pointStar:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(0, HEIGHT - PLAYER_HEIGHT)
        self.vel = random.randint(5, 10)

    def move(self):
        self.x -= self.vel

    def draw(self):
        WIN.blit(point_star, (self.x, self.y))

def drawWindow(Player, floor, enemies, points):
    WIN.blit(BG, (0, 0))
    player_health_text = HEALTH_FONT.render("Health: " + str(player_health), True, (232, 113, 39))
    score_text = SCORE_FONT.render("Score: " + str(score), True, (232, 113, 39))
    pygame.draw.rect(WIN, GRASS_GREEN, floor)

    if facing_left:
        WIN.blit(player_image_left, (Player.x, Player.y))
    else:
        WIN.blit(player_image_right, (Player.x, Player.y))
    WIN.blit(player_health_text, (70, 10))
    WIN.blit(score_text, (850, 10))

    for enemy in enemies:
        enemy.draw()

    for point in points:
        point.draw()

    pygame.display.update()

def collision(player, enemies, player_health):
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_WIDTH, ENEMY_HEIGHT)
        if player.colliderect(enemy_rect) and player_health > 0:
            return True
    return False

def scoreUpdate(player, points, player_health):
    for point in points:
        point_rect = pygame.Rect(point.x, point.y, POINT_WIDTH, POINT_WIDTH)
        if player.colliderect(point_rect) and player_health > 0:
            points.remove(point)
            return True
    return False

def movement(keys_pressed, Player, jumping, floor, jumpVel):
    global facing_left
    if keys_pressed[pygame.K_a] and Player.x - VEL > 0:  # left
        Player.x -= VEL
        facing_left = True
    if keys_pressed[pygame.K_d] and Player.x + VEL + Player.width < WIDTH:  # right
        Player.x += VEL
        facing_left = False

    # jumping mechanism
    if keys_pressed[pygame.K_SPACE] and Player.y - VEL > 0:
        jumping = True

    if jumping:
        Player.y -= jumpVel
        jumpVel -= 1

        # Check if the player has landed
        if Player.y + Player.height >= HEIGHT - floor.height:
            jumping = False
            Player.y = HEIGHT - floor.height - Player.height
    else:
        # Gravity effect when not jumping
        if Player.y + Player.height < HEIGHT - floor.height:
            Player.y += VEL

# ------------------------------------------MAIN MENU AND OPTIONS LOOP---------------------------------------------------------------
#global click

def options():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        WIN.fill((176, 245, 244))
        mute_button = pygame.Rect(WIDTH//2 - 100, 300, 200, 50)
        pygame.draw.rect(WIN, (235, 195, 52), mute_button)
        mute_text = MAIN_MENU_FONT.render("Mute", True, (255, 255, 255))
        WIN.blit(mute_text, (mute_button.x + (mute_button.width - mute_text.get_width()) // 2, mute_button.y + 
                             (mute_button.height - mute_text.get_height()) // 2))  # Corrected line

        pygame.display.update()
        clock.tick(FPS)
        

#click = False
clock = pygame.time.Clock()

#def mute_music(mute_button, mx, my, mute):
    #mute = False
    #pygame.mixer.music.play(-1)
    #if mute_button.collidepoint((mx, my)):
            #if click:
              #  mute = True
              #  pygame.mixer.music.pause()



def main_menu():
    while True:
        pygame.mixer.music.pause()
        WIN.fill((176, 245, 244))
        menu_text = MAIN_MENU_FONT.render("Fly-Away Cat Main Menu", True, (255, 255, 255))
        WIN.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, 100))
        mx, my = pygame.mouse.get_pos()


        button_1 = pygame.Rect(WIDTH//2 - 100, 300, 200, 50)
        button_2 = pygame.Rect(WIDTH//2 - 100, 400, 200, 50)
        
        if button_1.collidepoint((mx, my)):
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        pygame.draw.rect(WIN, (255, 0, 0), button_1)
        pygame.draw.rect(WIN, (0, 255, 0), button_2)

        play_text = MAIN_MENU_FONT.render("Play", True, (255, 255, 255))
        options_text = MAIN_MENU_FONT.render("Options", True, (255, 255, 255))
        
        WIN.blit(play_text, (button_1.x + (button_1.width - play_text.get_width()) // 2, button_1.y + (button_1.height - play_text.get_height()) // 2))  # Corrected line
        WIN.blit(options_text, (button_2.x + (button_2.width - options_text.get_width()) // 2, button_2.y + (button_2.height - options_text.get_height()) // 2))  # Corrected line

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)

#def gameOver():
    
# ----------------------------------------------MAIN GAME FUNCTION----------------------------------------------------------------------------

def main():
    pygame.mixer.music.play(-1)
    Player = pygame.Rect(10, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)  # player base
    floor = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)  # floor base

    enemies = []
    points = []
    global player_health
    global score
    player_health = 3
    score = 0

    player_visible = True

    run = True
    while run and player_health > 0:
        clock.tick(FPS)
        for event in pygame.event.get():  # this whole block runs game in 60 fps and allows you to exit game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == timer_event_id:
                player_visible = True
                pygame.time.set_timer(timer_event_id, 0)

        keys_pressed = pygame.key.get_pressed()  # to allow key binding
        movement(keys_pressed, Player, jumping, floor, jumpVel)  # calling on movement

        if random.randint(0, 100) < 5:  # Adjust the probability to control how often new enemies are created
            enemies.append(Enemy())

        if random.randint(0, 200) < 1:  # Adjust the probability to control how often new enemies are created
            points.append(pointStar())

        # Move and draw enemies
        for enemy in enemies:
            enemy.move()

        for point in points:
            point.move()

        # Check collision with enemies
        if collision(Player, enemies, player_health) and player_visible:
            player_health -= 1
            player_visible = False
            pygame.time.set_timer(timer_event_id, timer_interval)
            if (player_health >= 1):
                damage_sfx.play()

        if scoreUpdate(Player, points, player_health) and player_visible:
            score += 1
            point_sfx.play()

        # Remove off-screen enemies
        enemies = [enemy for enemy in enemies if enemy.x + ENEMY_WIDTH > 0]

        points = [point for point in points if point.x + POINT_WIDTH > 0]

        # Check player collision with floor
        if Player.colliderect(floor):
            Player.y = floor.y - Player.height

        drawWindow(Player, floor, enemies, points)

if __name__ == "__main__":
    main_menu()
