import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

#screen size
WIDTH, HEIGHT = 1920, 1020

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#title
pygame.display.set_caption("GAME")

#fps
FPS = 60

#velocity / movement
VEL = 10

#screen color / sky
SKY = (100, 255, 255)
GRASS_GREEN = (34, 177, 76) #grass color

#player dimensions
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 150          

#enemy dimensions
ENEMY_HEIGHT = 80
ENEMY_WIDTH = 90 

#jumping
jumping = False
jumpVel = 10

#for facing left
facing_left = False

#text font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

#invinc after collide so health doesnt drop

timer_interval = 1500 # 1.5 seconds
timer_event_id = pygame.USEREVENT + 1
global player_health


#player image facing right
player_image_right_path = pygame.image.load(os.path.join('PixelCat_right.png')) #loading from path
player_image_right = pygame.transform.scale(player_image_right_path, (PLAYER_WIDTH, PLAYER_HEIGHT))
#player image facing left
player_image_left_path = pygame.image.load(os.path.join('PixelCat_left.png'))
player_image_left = pygame.transform.scale(player_image_left_path, (PLAYER_WIDTH, PLAYER_HEIGHT))
#background
background_path = pygame.image.load(os.path.join('Background.png')).convert()
BG = pygame.transform.scale(background_path, (WIDTH, HEIGHT))
#enemy cat
neon_enemy_path = pygame.image.load(os.path.join('neon_enemy.png'))    
neon_enemy = pygame.transform.scale(neon_enemy_path,(ENEMY_WIDTH, ENEMY_HEIGHT))

class Enemy:
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(0, HEIGHT - PLAYER_HEIGHT)
        self.vel = random.randint(5, 10)


    def move(self):
        self.x -= self.vel
    
    def draw(self):
        WIN.blit(neon_enemy, (self.x, self.y))

def drawWindow(Player, floor, enemies):   #method for drawing window and coloring
    WIN.blit(BG, (0,0))
    player_health_text = HEALTH_FONT.render("Health: " + str(player_health), 1 , (232, 113, 39))
    pygame.draw.rect(WIN, GRASS_GREEN, floor)

    if facing_left:
        WIN.blit(player_image_left, (Player.x, Player.y))
    else:
        WIN.blit(player_image_right, (Player.x, Player.y))
    WIN.blit(player_health_text, (850,10))

    for enemy in enemies:
        enemy.draw()

    pygame.display.update()


def collision(player, enemies, player_health):
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_WIDTH, ENEMY_HEIGHT)
        if player.colliderect(enemy_rect) and player_health > 0:
            return True
    return False

def movement(keys_pressed, Player, jumping, floor, jumpVel):   #for moving character
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
    


def main():

    Player = pygame.Rect(10, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) # player base
    floor = pygame.Rect(0, HEIGHT - 50, WIDTH, 50) # floor base

    enemies = []
    global player_health
    player_health = 3
    
    player_visible = True

    clock = pygame.time.Clock()
    run = True
    while run and player_health > 0:
        clock.tick(FPS)
        for event in pygame.event.get():     # this whole block runs game in 60 fps and allows you to exit game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == timer_event_id:
                player_visible = True
                pygame.time.   set_timer(timer_event_id, 0)
        
        keys_pressed = pygame.key.get_pressed() # to allow key binding
        movement(keys_pressed, Player, jumping, floor, jumpVel)  #calling on movement

        if random.randint(0, 100) < 5:  # Adjust the probability to control how often new enemies are created
            enemies.append(Enemy())

        # Move and draw enemies
        for enemy in enemies:
            enemy.move()

        # Check collision with enemies
        if collision(Player, enemies, player_health) and player_visible:
            player_health -= 1
            player_visible = False
            pygame.time.set_timer(timer_event_id, timer_interval) 

        # Remove off-screen enemies
        enemies = [enemy for enemy in enemies if enemy.x   + ENEMY_WIDTH > 0]

        # Check player collision with floor
        if Player.colliderect(floor): 
            Player.y = floor.y - Player.height

        drawWindow(Player, floor, enemies)

main()

if __name__ == "__main__":
    main()
