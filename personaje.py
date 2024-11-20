# planta.py (archivo completo)
import pygame
import constantes

class Planta:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA)
        self.tiempo_plantado = pygame.time.get_ticks()
        self.estado = 0  # 0: semilla, 1: crecimiento, 2: maduro
        
        try:
            # Cargar sprites de arroz
            self.sprites = [
                pygame.image.load("assets//image//crops//arroz_1.png").convert_alpha(),
                pygame.image.load("assets//image//crops//arroz_2.png").convert_alpha(),
                pygame.image.load("assets//image//crops//arroz_3.png").convert_alpha()
            ]
            
            # Escalar sprites
            self.sprites = [pygame.transform.scale(sprite, (constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA)) 
                           for sprite in self.sprites]
        except:
            # Si no se encuentran las imágenes, usar rectángulos de colores
            self.usar_rectangulos = True
            self.colores = [(139, 69, 19), (34, 139, 34), (0, 100, 0)]  # Marrón, Verde, Verde oscuro
        else:
            self.usar_rectangulos = False

    def update(self):
        tiempo_actual = pygame.time.get_ticks() - self.tiempo_plantado
        
        if tiempo_actual >= constantes.TIEMPO_CRECIMIENTO * 2:
            self.estado = 2
        elif tiempo_actual >= constantes.TIEMPO_CRECIMIENTO:
            self.estado = 1

    def draw(self, surface):
        if self.usar_rectangulos:
            pygame.draw.rect(surface, self.colores[self.estado], self.rect)
        else:
            surface.blit(self.sprites[self.estado], self.rect)

# personaje.py (archivo completo)
import pygame
import constantes
from planta import Planta

class Personaje():
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x,y)
        self.moviendo = False
        self.direccion = None
        self.plantas = []
        self.huecos = []

    def movimiento(self, delta_x, delta_y):
        if delta_x != 0 or delta_y != 0:
            self.moviendo = True
        else:
            self.moviendo = False

        if delta_x < 0:
            self.flip = False
            self.direccion = 'izquierda'
        if delta_x > 0:
            self.flip = True
            self.direccion = 'derecha'
        if delta_y < 0:
            self.direccion = 'arriba'
        if delta_y > 0:
            self.direccion = 'abajo'

        self.forma.x += delta_x
        self.forma.y += delta_y

    def crear_hueco(self, pos_x, pos_y):
        for zona in constantes.ZONAS_CULTIVO:
            nuevo_hueco = pygame.Rect(pos_x, pos_y, constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA)
            if zona.colliderect(nuevo_hueco):
                self.huecos.append(nuevo_hueco)
                return True
        return False

    def cultivar(self, zonas_cultivo):
        # Primero verificar si está en una zona de cultivo
        en_zona_cultivo = False
        for zona in zonas_cultivo:
            if self.forma.colliderect(zona):
                en_zona_cultivo = True
                break
                
        if not en_zona_cultivo:
            print("No estás en una zona de cultivo")
            return False

        # Si está en zona de cultivo, verificar huecos
        for hueco in self.huecos:
            if self.forma.colliderect(hueco):
                # Verificar si ya hay una planta en esta posición
                posicion_ocupada = False
                for planta in self.plantas:
                    if planta.rect.colliderect(hueco):
                        posicion_ocupada = True
                        break
                        
                if not posicion_ocupada:
                    nueva_planta = Planta(hueco.x, hueco.y)
                    self.plantas.append(nueva_planta)
                    print("¡Planta cultivada!")
                    return True
                else:
                    print("Ya hay una planta en este hueco")
                    return False
        
        print("Necesitas crear un hueco primero")
        return False

    def update(self):
        cooldown_animacion = 100
        if self.moviendo:
            if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animaciones):
                self.frame_index = 0
            self.image = self.animaciones[self.frame_index]
        else:
            self.image = self.animaciones[0]
        
        for planta in self.plantas:
            planta.update()

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        
        # Dibujar huecos
        for hueco in self.huecos:
            pygame.draw.rect(interfaz, (139, 69, 19), hueco, 2)  # Dibujar borde del hueco
            
        for planta in self.plantas:
            planta.draw(interfaz)
    
    def regar(self):
        for planta in self.plantas:
            if self.forma.colliderect(planta.rect):
                if planta.regar():
                    print("¡Planta regada!")
                    return True
        return False