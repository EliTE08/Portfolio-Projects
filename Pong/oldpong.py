import pygame
import time
import random
pygame.font.init()

#Screen -----------------------------------------------------------
WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

BG = pygame.transform.scale(pygame.image.load("Pong\\bg.jpg"), (WIDTH, HEIGHT))
# -----------------------------------------------------------------
# -----------------------------------------------------------------
#Game Variables ---------------------------------------------------
PLAYER_SCORE = 0
ENEMY_SCORE = 0

PLAYER_WIDTH, PLAYER_HEIGHT = 10, 75
PLAYER_VEL = 5

ENEMY_WIDTH, ENEMY_HEIGHT = 10, 75
ENEMY_VEL = 5.25

STAR_WIDTH = 15
STAR_HEIGHT = 15
STAR_RADIUS = 15
STAR_VEL = 3
# -------------------------------------------------------------------
# -------------------------------------------------------------------
#Font ---------------------------------------------------------------
FONT = pygame.font.SysFont("comicsans", 30)
# -------------------------------------------------------------------
# -------------------------------------------------------------------
#Draws stuff to the screen ------------------------------------------
def draw(player, elapsed_time, star, enemy, PLAYER_SCORE, ENEMY_SCORE):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (350, 10))

    player_score_text = FONT.render(f"Player: {PLAYER_SCORE}", 1, "white")
    WIN.blit(player_score_text, (100, 10))

    enemy_score_text = FONT.render(f"Enemy: {ENEMY_SCORE}", 1, "white")
    WIN.blit(enemy_score_text,(600, 10))

    pygame.draw.rect(WIN, "white", player)
    pygame.draw.rect(WIN, "red", star)
    pygame.draw.rect(WIN, "white", enemy)

    pygame.display.update()
# -------------------------------------------------------------------

def main(PLAYER_SCORE, ENEMY_SCORE):
    run = True

    hitx = False
    hity = False

    player = pygame.Rect(100, 250, PLAYER_WIDTH, PLAYER_HEIGHT)

    enemy = pygame.Rect(700, 250, ENEMY_WIDTH, ENEMY_HEIGHT)

    star = pygame.Rect(400, 250, STAR_WIDTH, STAR_HEIGHT)

    clock = pygame.time.Clock()
    elapsed_time=0

    speedmult = 0

    start = 1

    start_time = time.time()

    #Flips who the ball is fed to at first ------------------------------
    if((ENEMY_SCORE + PLAYER_SCORE) % 2 != 0):
        hitx=True
    # -------------------------------------------------------------------

    while run:
        
        #Starts game timer and fixes the -4 issue
        clock.tick(60)
        elapsed_time=time.time()-start_time-4
        if(elapsed_time<0):
            elapsed_time = 0

        #Checks if they have clicked the quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        #Checks elapsed time to add to speedmult
        if (round(elapsed_time, 1)%10 == 0):
            speedmult += 0.1

        #Movement for player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]:
            player.y += PLAYER_VEL
        if player.y <= 0:
            player.y = 0
        if player.y >= HEIGHT-PLAYER_HEIGHT:
            player.y = HEIGHT-PLAYER_HEIGHT

        #Movement for enemy
        if(enemy.y <= 0):
            enemy.y = 0
        if(enemy.y >= HEIGHT-ENEMY_HEIGHT):
            enemy.y = HEIGHT-ENEMY_HEIGHT
        if(star.y > enemy.y):
            enemy.y += ENEMY_VEL
        if(star.y < enemy.y):
            enemy.y -= ENEMY_VEL

        #Checks if star hits enemy
        if (star.x + star.height >= enemy.x and star.colliderect(enemy)):
            hitx = False

            #Changes which way the pong goes randomly
            randomint = random.randint(0, 10)
            if randomint <= 4:
                hity = not hity

        #Changes which way the pong moves
        if(hity==False):
            star.y += STAR_VEL + speedmult
        if(hity==True):
            star.y -= STAR_VEL + speedmult
        if(hitx==False):
            star.x -= STAR_VEL + speedmult
        if(hitx==True):
            star.x += STAR_VEL + speedmult

        #Checks if star hits player
        if (star.x + star.height >= player.x and star.colliderect(player)):
            hitx=True

            #Changes which way the pong goes randomly
            randomint = random.randint(0, 10)
            if randomint <= 4:
                hity = not hity
        
        #Checks if star hits ceiling or floor
        if (star.y + star.height >= HEIGHT):
            hity = True
        if (star.y <= 0):
            hity = False

        #Checks if star hits wall and adds score
        if (star.x + star.width <= 0):
            ENEMY_SCORE += 1
            main(PLAYER_SCORE, ENEMY_SCORE)
        if (star.x + star.width >= WIDTH):
            PLAYER_SCORE += 1
            main(PLAYER_SCORE, ENEMY_SCORE)
        
        #Calls draw function
        draw(player, elapsed_time, star, enemy, PLAYER_SCORE, ENEMY_SCORE)


        #Delays the start
        if(start == 1):
            pygame.time.delay(4000)
            start+=1
    
    pygame.quit()

if __name__ == "__main__":
    main(PLAYER_SCORE, ENEMY_SCORE)