import pygame
import constantes

class Planta:
    # Contador de plantas por zona (clase compartida entre todas las plantas)
    plantas_por_zona = {i: 0 for i in range(len(constantes.ZONAS_CULTIVO))}

    def __init__(self, x, y, zona, tipo='arroz'):
        self.rect = pygame.Rect(x, y, constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA)
        self.estado = 0  # 0: semilla, 1: crecimiento, 2: maduro
        self.necesita_agua = True
        self.cambio_fase_pendiente = False
        self.tiempo_inicio_cambio = 0
        self.zona = zona  # Zona donde está la planta
        self.tipo = tipo
        self.info = constantes.INFO_CULTIVOS[tipo]
        self.veces_regada = 0
        self.salud = 100

        try:
            # Sprites de la planta
            self.sprites = [
                pygame.image.load("assets//image//crops//arroz_1.png").convert_alpha(),
                pygame.image.load("assets//image//crops//arroz_2.png").convert_alpha(),
                pygame.image.load("assets//image//crops//arroz_3.png").convert_alpha()
            ]
            self.sprites = [pygame.transform.scale(sprite, (constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA)) 
                            for sprite in self.sprites]
            # Imagen del terreno
            self.terreno = pygame.image.load("assets//image//tierra.png").convert_alpha()
            self.terreno = pygame.transform.scale(self.terreno, (constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA))
            self.usar_rectangulos = False
        except:
            self.usar_rectangulos = True
            self.colores = [(139, 69, 19), (34, 139, 34), (0, 100, 0)]

    @classmethod
    def agregar_planta(cls, x, y):
        # Verifica si las coordenadas están dentro de una zona válida
        for i, zona in enumerate(constantes.ZONAS_CULTIVO):
            if zona.collidepoint(x, y):
                # Comprueba si se ha alcanzado el límite de plantas en esta zona
                if cls.plantas_por_zona[i] < constantes.MAX_PLANTAS_POR_ZONA:
                    cls.plantas_por_zona[i] += 1
                    return Planta(x, y, i)
                else:
                    print("Límite de plantas alcanzado en esta zona.")
                    return None
        print("No está en una zona válida para plantar.")
        return None

    def regar(self):
        if self.necesita_agua and not self.cambio_fase_pendiente and self.estado < 2:
            self.necesita_agua = False
            self.cambio_fase_pendiente = True
            self.tiempo_inicio_cambio = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        if self.cambio_fase_pendiente:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_inicio_cambio >= constantes.TIEMPO_CAMBIO_FASE:
                if self.estado < 2:
                    self.estado += 1
                    self.necesita_agua = True
                    self.cambio_fase_pendiente = False
                    if self.estado == 2:
                        return "completado"  # La planta está completamente madura
        return None

    def draw(self, surface):
        if not self.usar_rectangulos:
            surface.blit(self.terreno, self.rect)
        else:
            pygame.draw.rect(surface, (160, 82, 45), self.rect) 

        # Dibuja la planta
        if self.usar_rectangulos:
            pygame.draw.rect(surface, self.colores[self.estado], self.rect)
            if self.necesita_agua:
                pygame.draw.rect(surface, (0, 0, 255), self.rect, 2)
        else:
            surface.blit(self.sprites[self.estado], self.rect)
            if self.necesita_agua:
                pygame.draw.rect(surface, (0, 0, 255), self.rect, 2)  # Borde azul si necesita agua