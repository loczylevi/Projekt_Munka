# Könyvtárak beimportálása
import pygame
from random import randint
 
FEKETE = (0, 0, 0)
 
class Ball(pygame.sprite.Sprite):
    # Ez a class a labdát foglya irányítani, szabáylozni
    def __init__(self, color, width, height):
        super().__init__()
        
        # A labda paramétereinkek megadása: szine, szélessége, magassága
        self.image = pygame.Surface([width, height])
        self.image.fill(FEKETE)
        self.image.set_colorkey(FEKETE)
 
        # Labda rajzolása (négyzet)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [7,-7]
        
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
          
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(5,7)