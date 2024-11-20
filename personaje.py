import pygame
import constantes
from planta import Planta

class Personaje:
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.centerx = x
        self.forma.centery = y
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

        # Usar centerx/centery para un movimiento más suave y centrado
        self.forma.centerx += delta_x
        self.forma.centery += delta_y

    def crear_hueco(self, pos_x, pos_y):
        for i, zona in enumerate(constantes.ZONAS_CULTIVO):
            if zona.collidepoint(pos_x, pos_y):
                # Verificar si ya hay 4 huecos en esta zona
                huecos_en_zona = sum(1 for hueco in self.huecos if zona.collidepoint(hueco[0], hueco[1]))
                if huecos_en_zona >= 4:
                    print("Esta zona ya tiene el máximo de huecos permitidos (4)")
                    return False

                # Calcular posiciones predefinidas en la zona
                filas = (zona.height // constantes.TAMANO_PLANTA)
                columnas = (zona.width // constantes.TAMANO_PLANTA)
                
                # Encontrar la posición más cercana en la cuadrícula
                col = min(max(0, (pos_x - zona.x) // constantes.TAMANO_PLANTA), columnas - 1)
                fila = min(max(0, (pos_y - zona.y) // constantes.TAMANO_PLANTA), filas - 1)
                
                hueco_x = zona.x + (col * constantes.TAMANO_PLANTA)
                hueco_y = zona.y + (fila * constantes.TAMANO_PLANTA)
                
                # Verificar si ya existe una planta en esta posición
                for planta in self.plantas:
                    if planta.rect.collidepoint(hueco_x, hueco_y):
                        print("Ya existe una planta en esta posición")
                        return False
                
                # Crear la planta en la posición predefinida
                nueva_planta = Planta(hueco_x, hueco_y)
                self.plantas.append(nueva_planta)
                print(f"¡Planta creada en posición [{col},{fila}]!")
                return True
                
        print("No se puede plantar fuera de las zonas de cultivo")
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
        # Asegurar que la imagen se dibuje centrada en su posición
        rect_centrado = imagen_flip.get_rect(center=self.forma.center)
        interfaz.blit(imagen_flip, rect_centrado)
        
        # Dibujar huecos
        for hueco in self.huecos:
            rect_hueco = pygame.Rect(hueco[0], hueco[1], constantes.TAMANO_PLANTA // 3, constantes.TAMANO_PLANTA // 3)
            pygame.draw.rect(interfaz, (139, 69, 19), rect_hueco, 2)  # Dibujar borde del hueco más pequeño
            
        for planta in self.plantas:
            planta.draw(interfaz)
    
    def regar(self):
        for planta in self.plantas:
            if self.forma.colliderect(planta.rect):
                if planta.regar():
                    print("¡Planta regada!")
                    return True
        return False