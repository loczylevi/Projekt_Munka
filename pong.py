# könyvtárak beimportálása
import pygame
from paddle import Paddle
from ball import Ball
import time
import cv2
import mediapipe as mp
from pygame import display, movie

# ablak készitése
pygame.init()

# Szinek megadása
FEKETE = (0, 0, 0)
FEHER = (255, 255, 255)

# Kamera ablak létrehozása:
cap = cv2.VideoCapture(0)

# Kéz felismerés
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# A játék ablak létrehozása
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("image")

# 1. Játékos paraméterek megadása 
paddleA = Paddle(FEHER, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

# 2. Játékos paraméterek megadása 
paddleB = Paddle(FEHER, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

# Labda paraméterek megadása
ball = Ball(FEHER, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# Lista mely tartalmazza a játék összes elemeket
all_sprites_list = pygame.sprite.Group()

# Hozzáad 2 játékost és egy labdát egy listához
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# Addig fog a ciklus menni míg a játékos meg nem nyomja a bezáró gombot
carryOn = True

# Az óra arra lesz hasznos irányitsuk a képernyő frissitését (FPS)
clock = pygame.time.Clock()

# Megadjuk a játékosok ponjait
scoreA = 0
scoreB = 0
valtozo = True

# kamera
mpDraw = mp.solutions.drawing_utils

# fps változok
pTime = 0
cTime = 0

# --- A program fő ciklusa, A program szive 
while carryOn:

    if valtozo == False:
        time.sleep(2)
        # 2 másodpercet vár egy pont szerzés után (Játékosnak legyen ideje felkészülni)
        valtozo = True

    for event in pygame.event.get():  # A felhasználó csinált valamit
        if event.type == pygame.QUIT:  # Ha a játékos kilép a játékból
            carryOn = False  # Mivel átirtuk a változonak az értékét kitör a ciklusból
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Az "x" gomb lenyomásával kilép a játékból
                carryOn = False
    # ------------------------------------------------------------------------------------------
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # 1. játékos irányitása
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):    
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)       # A kéz x(szélesség), y(magasság) Kordinációk vizsgálása
                if 300 < cx < 690:                          # ha eközött az értéken belül van a kezünk a játékos mozog
                    paddleA.rect.y = cy
    # 2. játékos irányitása               
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for ko, fa in enumerate(handLms.landmark):
                z, s, n = img.shape        
                nb, nj = int(fa.x * s), int(fa.y * z)     # A kéz b(szélesség), j(magasság) Kordinációk vizsgálása
                if -50 < nb < 300:                        #ha eközött az értéken belül van a kezünk a játékos mozog
                    paddleB.rect.y = nj  
            # ------------------------------------------------------------------------------------------
            # A kéz pontjain jelölöket rajzolunk
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    #frissités
    all_sprites_list.update()

    # Megnézzük hozáért-e a labda valamelyik falhoz
    if ball.rect.x >= 690:
        scoreA += 1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        paddleA.rect.x = 20
        paddleA.rect.y = 200
        paddleB.rect.x = 670
        paddleB.rect.y = 200
        valtozo = False
    if ball.rect.x <= 0:
        scoreB += 1
        ball.velocity[0] = -ball.velocity[0]
        ball.rect.x = 345
        ball.rect.y = 195
        paddleA.rect.x = 20
        paddleA.rect.y = 200
        paddleB.rect.x = 670
        paddleB.rect.y = 200
        valtozo = False
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]
    if scoreA == 10 or scoreB == 10:
        break
    # Viszgálunk az ütközésre a labda és a játékos között
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    # Elöször feketére változatjuk a képernyőt
    screen.fill(FEKETE)
    
    # A középső vonal rajzolás
    pygame.draw.line(screen, FEHER, [349, 0], [349, 500], 5)

    # Lerajzoljuk a karaktereket 
    all_sprites_list.draw(screen)

    # A pontszám megjelenitése
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, FEHER)
    screen.blit(text, (250, 10))
    text = font.render(str(scoreB), 1, FEHER)
    screen.blit(text, (420, 10))

    # Változások lerajzolása
    pygame.display.flip()

    # --- 60 kép/ másodpercenként FPS
    clock.tick(60)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("image", img)
    cv2.waitKey(1)
    
# kilépünk a játékból
pygame.quit()