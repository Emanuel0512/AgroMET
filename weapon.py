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
        self.inventario = None
    
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

    def shoot(self, direccion):
        self.disparada = True
        velocidad = 10
        if direccion == 'derecha':
            self.velocidad_x = velocidad
            self.velocidad_y = 0
        elif direccion == 'izquierda':
            self.velocidad_x = -velocidad
            self.velocidad_y = 0
        elif direccion == 'arriba':
            self.velocidad_x = 0
            self.velocidad_y = -velocidad
        elif direccion == 'abajo':
            self.velocidad_x = 0
            self.velocidad_y = velocidad

    def dibujar(self, interfaz):
        interfaz.blit(self.imagen, self.forma)

class Hoz:
    def __init__(self, image):
        self.imagen_original = pygame.transform.scale(image, 
            (image.get_width() * constantes.SCALA_HOZ, 
             image.get_height() * constantes.SCALA_HOZ))
        self.angulo = 0
        self.imagen = self.imagen_original
        self.forma = self.imagen.get_rect()
        self.flip = False
        
    def update(self, personaje):
        self.forma.center = personaje.forma.center
        if personaje.direccion == 'derecha':
            self.angulo = 0
            self.flip = False
            offset_x, offset_y = 10, 20
        elif personaje.direccion == 'izquierda':
            self.angulo = 0
            self.flip = True
            offset_x, offset_y = -10, 20
        else:
            offset_x = 10 if not self.flip else -10
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

class WateringCan:
    def __init__(self, image):
        self.imagen_original = image
        self.angulo = 0
        self.imagen = self.imagen_original
        self.forma = self.imagen.get_rect()
        self.flip = False
        self.disparada = False
        self.velocidad_x = 0
        self.velocidad_y = 0
        
    def update(self, personaje):
        self.forma.center = personaje.forma.center
        if personaje.direccion == 'derecha':
            self.angulo = 0
            self.flip = False
            offset_x, offset_y = 10, 20
        elif personaje.direccion == 'izquierda':
            self.angulo = 0
            self.flip = True
            offset_x, offset_y = -10, 20
        else:
            offset_x = 10 if not self.flip else -10
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
      self.frames = [
          pygame.image.load("assets//image//bullets//bullet1.png").convert_alpha(),
          pygame.image.load("assets//image//bullets//bullet2.png").convert_alpha(),
          pygame.image.load("assets//image//bullets//bullet3.png").convert_alpha()
      ]
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()
      self.angulo = angle
      self.image = pygame.transform.rotate(self.frames[self.frame_index], self.angulo)
      self.rect = self.image.get_rect()
      self.rect.center = (x,y)
      self.delta_x = math.cos(math.radians(self.angulo))*constantes.VELOCIDAD_BALA
      self.delta_y = -math.sin(math.radians(self.angulo))*constantes.VELOCIDAD_BALA

    def update(self):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        
        # Actualizar animación
        animation_cooldown = 100  # milisegundos entre frames
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = pygame.transform.rotate(self.frames[self.frame_index], self.angulo)
            self.update_time = pygame.time.get_ticks()
            
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()

    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery -int(self.image.get_height()/2)))