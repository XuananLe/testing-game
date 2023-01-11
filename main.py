import pygame
import os
pygame.font.init()
pygame.mixer.init()
#tao ra font
HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

WIDTH, HEIGHT = 900, 900
#set up window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#set title cho man hinh
pygame.display.set_caption("First game like that")
#tao ra mau
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
#frame per second
FPS = 60
VEL = 5 
SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 55
BULLET_VEL = 7
MAX_BULLETS_AT_A_TIME = 3
#tao ra border giua 2 space ship
BORDER = pygame.Rect(435,0,10,900)

#tao ra 2 event de phan biet 2 cai dan ???
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


#load va rotate va scale lai image
YELLOW_SPACESHIP = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP,90)
RED_SPACESHIP = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP,-90)

SPACE = pygame.image.load(os.path.join('Assets','space.png'))
SPACE = pygame.transform.scale(SPACE, (900,900))

#tao ra sound cho bullet
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

def draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH):
    #blit use to draw surface into the window
    WIN.blit(SPACE, (0,0))
    #ve border
    pygame.draw.rect(WIN,WHITE,BORDER)
    #ve yellow health va red health
    red_health_text = HEALTH_FONT.render("HEALTH: " + str(RED_HEALTH), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(YELLOW_HEALTH), 1, WHITE)
    WIN.blit(red_health_text,(900 - red_health_text.get_width() - 10,10))
    WIN.blit(yellow_health_text,(10,10))

    #fill yellow_spaceship vao yellow rectangle
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()

#yellow ben trai, red ben phai, xu li di chuyen voi 2 ben
def draw_winner(text):
    WIN.blit(SPACE, (0,0))
    winner_text = HEALTH_FONT.render(text + "WIN", 1, WHITE)
    WIN.blit(winner_text, (450 - winner_text.get_width() / 2, 450 - winner_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)


def handle_red(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x >= 444:
        red.x -= VEL
    if(key_pressed[pygame.K_RIGHT]) and red.x < 845:
        red.x += VEL
    if key_pressed[pygame.K_DOWN] and red.y < 860:
        red.y += VEL
    if(key_pressed[pygame.K_UP]) and red.y - VEL >0:
        red.y -= VEL

def handle_yellow(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x >= 3:
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x <= 380:
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y >= 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y <= 845:
        yellow.y += VEL

def handleBullets(red_bullets, yellow_bullets,red,yellow): 
    for bullets in yellow_bullets:
        bullets.x += BULLET_VEL
        #check xem red co cham vao bullet hay khong, k biet co dung duoc mang trong C++ khong :vvv can viet them ham ve rect
        if red.colliderect(bullets):
            #neu trung muc tieu se remove
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullets)
        elif bullets.x > 845:
            yellow_bullets.remove(bullets)
    for bullets in red_bullets:
        bullets.x -= BULLET_VEL
        if yellow.colliderect(bullets):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullets)
        elif bullets.x < 0:
            red_bullets.remove(bullets)


def main():
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    winne_text = ""
    clock = pygame.time.Clock()
    #kha nang cao la de initialized spaceship pos, giong nhu class
    yellow = pygame.Rect(0,450, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(840,450, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    #red player bullets
    red_bullets = []
    #yellow player bullets
    yellow_bullets = []
    run = True
    while run:
        clock.tick(FPS)
         #handle multiple key pressed
        keys_pressed = pygame.key.get_pressed()
        handle_red(keys_pressed,red)
        handle_yellow(keys_pressed, yellow)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # dung de check xem con du dan khong, python la l vl
                if event.key == pygame.K_z and len(yellow_bullets) < MAX_BULLETS_AT_A_TIME:
                    bullet = pygame.Rect(yellow.x + yellow.width - 3,yellow.y + yellow.height/2 -2,
                    10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_m and len(red_bullets) < MAX_BULLETS_AT_A_TIME:
                    bullet = pygame.Rect(red.x, red.y + red.height/2 -2,
                    10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            #neu nhu == red_hit thi tru 1 health ?? dell hieu kieu j
            winner_text = ""
            if event.type == RED_HIT:
                RED_HEALTH -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -=1 
                BULLET_HIT_SOUND.play()
            if YELLOW_HEALTH <= 0:
                winner_text = "RED"
            if RED_HEALTH <= 0:
                winner_text = "YELLOW"
            if winner_text != "":
                run = False
        handleBullets(red_bullets, yellow_bullets,red,yellow)
        draw_window(red,yellow,red_bullets,yellow_bullets,RED_HEALTH, YELLOW_HEALTH) 
    draw_winner(winner_text)
    pygame.quit()
if __name__ == "__main__":
    main()
