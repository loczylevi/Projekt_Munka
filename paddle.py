# Könyvtár beimportálása
import pygame
FEKETE = (0,0,0)
 
class Paddle(pygame.sprite.Sprite):
    # Ez a class a játékos értékeivel foglalkozik, szabályozza
    
    def __init__(self, color, width, height):
        super().__init__()
        
        # A játékos paramétereinkek megadása: szine, szélessége, magassága
        self.image = pygame.Surface([width, height])
        self.image.fill(FEKETE)
        self.image.set_colorkey(FEKETE)
 
        # Játékos rajzolása
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.rect = self.image.get_rect()
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
        # Viszgálnuk arra, hogy nem lépünk ki a képernyőböl
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
        # Viszgálnuk arra, hogy kilépünk a képernyőböl
        if self.rect.y > 400:
          self.rect.y = 400
    