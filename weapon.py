import pygame
import constantes
import math

class Pala:
    def __init__(self, image, bala_image):
        self.imagen_original = image
        self.bala_image = bala_image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
    
    def update(self, personaje):
        self.forma.center = personaje.forma.center
        if personaje.flip:
            self.forma.x += personaje.forma.width - 67
            self.forma.y += personaje.forma.width - 55
            self.rotar_herramienta(False)
        else:
            self.forma.x -= personaje.forma.width - 65
            self.forma.y -= personaje.forma.width - 95
            self.rotar_herramienta(True)

    def rotar_herramienta(self, rotar):
        if rotar:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)

class WateringCan:
    def __init__(self, image):
        self.imagen_original = image
        self.angulo = 0
        self.imagen = self.imagen_original
        self.forma = self.imagen.get_rect()
        self.flip = False
        
    def update(self, personaje):
        self.forma.center = personaje.forma.center
        if personaje.direccion == 'derecha':
            self.angulo = -90
            self.flip = False
            offset_x, offset_y = 30, 20
        elif personaje.direccion == 'izquierda':
            self.angulo = 90
            self.flip = True
            offset_x, offset_y = -30, 20
        elif personaje.direccion == 'arriba':
            self.angulo = 180
            self.flip = False
            offset_x, offset_y = 0, -20
        elif personaje.direccion == 'abajo':
            self.angulo = 0
            self.flip = False
            offset_x, offset_y = 0, 40
        else:
            offset_x = 30 if not self.flip else -30
            offset_y = 20
            
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        if self.flip:
            self.imagen = pygame.transform.flip(self.imagen, True, False)
            
        self.forma = self.imagen.get_rect()
        self.forma.center = personaje.forma.center
        self.forma.x += offset_x
        self.forma.y += offset_y
        
    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
      pygame.sprite.Sprite.__init__(self)
      self.imagen_original = image
      self.angulo = angle
      self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
      self.rect = self.image.get_rect()
      self.rect.center = (x,y)
      self.delta_x = math.cos(math.radians(self.angulo))*constantes.VELOCIDAD_BALA
      self.delta_y = -math.sin(math.radians(self.angulo))*constantes.VELOCIDAD_BALA

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()

    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery -int(self.image.get_height()/2)))