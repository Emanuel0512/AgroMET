import pygame
import constantes

class Planta:
    # Contador de plantas por zona (clase compartida entre todas las plantas)
    plantas_por_zona = {i: 0 for i in range(len(constantes.ZONAS_CULTIVO))}

    def __init__(self, x, y, zona=None, tipo='arroz'):
        self.recolectada = False
        self.visible = True  # Aseguramos que inicie visible
        self.mensaje_puntos = None
        self.tiempo_mensaje = 0
        self.rect = pygame.Rect(x, y, constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA)
        self.estado = 0  # 0: semilla, 1: crecimiento, 2: maduro
        self.necesita_agua = True
        self.cambio_fase_pendiente = False
        self.tiempo_inicio_cambio = pygame.time.get_ticks()
        self.tiempo_ultimo_cambio = self.tiempo_inicio_cambio
        self.tiempo_entre_estados = 10000  # 10 segundos entre estados
        self.puede_crecer = True  # Control de crecimiento
        
        # Colores para el modo de dibujo con rectángulos
        self.colores = [(139, 69, 19), (34, 139, 34), (0, 100, 0)]  # Marrón, Verde claro, Verde oscuro
        self.color_tallo = (85, 107, 47)  # Verde oliva
        self.color_hojas = (34, 139, 34)  # Verde forestall 
        self.color_arroz = (255, 250, 205)  # Amarillo claro
        
        # Variables para reproducción
        self.puede_reproducirse = False
        self.ultimo_tiempo_reproduccion = pygame.time.get_ticks()
        self.semillas_producidas = 0
        self.max_semillas = 3
        self.zona = zona  # Zona donde está la planta
        self.tipo = tipo
        self.info = constantes.INFO_CULTIVOS[tipo]
        self.veces_regada = 0
        self.salud = 100
        self.usar_rectangulos = False
        self.mensaje_puntos = None
        self.tiempo_mensaje = 0
        
        # Colores para el modo de respaldo
        self.colores = [(139, 69, 19), (34, 139, 34)]  # Marrón para tierra, verde para planta
        self.color_tallo = (0, 100, 0)  # Verde oscuro
        self.color_hojas = (0, 150, 0)  # Verde medio
        self.color_arroz = (255, 223, 186)  # Color crema para el arroz

        # Imagen del terreno
        self.terreno = pygame.image.load("assets/image/hueco.png").convert_alpha()
        self.terreno = pygame.transform.scale(self.terreno, (int(constantes.TAMANO_PLANTA * 1.5), int(constantes.TAMANO_PLANTA * 1.5)))
        
        # Sprites de la planta según el tipo
        self.sprites = []
        sprite_paths = [f"assets/image/arroz_{i}.png" for i in range(3)]
        for path in sprite_paths:
            sprite_arroz = pygame.image.load(path).convert_alpha()
            sprite_arroz = pygame.transform.scale(sprite_arroz, (constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA))
            self.sprites.append(sprite_arroz)
        
        # Initialize visibility flag
        self.visible = True

    @classmethod
    def agregar_planta(cls, x, y):
        for i, zona in enumerate(constantes.ZONAS_CULTIVO):
            if zona.collidepoint(x, y):
                if cls.plantas_por_zona[i] < constantes.MAX_PLANTAS_POR_ZONA:
                    cls.plantas_por_zona[i] += 1
                    nueva_planta = Planta(x, y, i)
                    print(f"Plantas en zona {i}: {cls.plantas_por_zona[i]} de {constantes.MAX_PLANTAS_POR_ZONA}")
                    return nueva_planta
                else:
                    print(f"Límite de plantas alcanzado en esta zona ({constantes.MAX_PLANTAS_POR_ZONA} plantas).")
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
        tiempo_actual = pygame.time.get_ticks()
        
        # Verificar si es tiempo de cambiar de estado
        if self.puede_crecer and not self.necesita_agua:
            if tiempo_actual - self.tiempo_ultimo_cambio >= self.tiempo_entre_estados:
                if self.estado < len(self.sprites) - 1:
                    self.estado += 1
                    self.tiempo_ultimo_cambio = tiempo_actual
                    self.necesita_agua = True
                    print(f"Planta avanzó al estado {self.estado}")
                    if self.estado == len(self.sprites) - 1:
                        self.puede_reproducirse = True
                        return "completado"
        
        # Lógica de reproducción
        if self.puede_reproducirse and self.estado == len(self.sprites) - 1:
            if tiempo_actual - self.ultimo_tiempo_reproduccion >= constantes.TIEMPO_REPRODUCCION:
                self.reproducir()
                self.ultimo_tiempo_reproduccion = tiempo_actual
        
        # Procesar el riego
        if self.cambio_fase_pendiente:
            if tiempo_actual - self.tiempo_inicio_cambio >= constantes.TIEMPO_CAMBIO_FASE:
                self.cambio_fase_pendiente = False
                self.puede_crecer = True  # Permitir el siguiente crecimiento  

    def reproducir(self):
        if self.semillas_producidas >= self.max_semillas:
            return None
            
        import random
        import math
        for _ in range(constantes.MAX_INTENTOS_REPRODUCCION):
            # Generar posición aleatoria dentro del radio permitido
            angulo = random.uniform(0, 2 * math.pi)
            distancia = random.uniform(constantes.TAMANO_PLANTA, constantes.DISTANCIA_REPRODUCCION)
            nuevo_x = self.rect.x + int(distancia * math.cos(angulo))
            nuevo_y = self.rect.y + int(distancia * math.sin(angulo))
            
            # Verificar si la posición está dentro de una zona de cultivo
            for i, zona in enumerate(constantes.ZONAS_CULTIVO):
                if zona.collidepoint(nuevo_x, nuevo_y):
                    if self.plantas_por_zona[i] < constantes.MAX_PLANTAS_POR_ZONA:
                        self.plantas_por_zona[i] += 1
                        self.semillas_producidas += 1
                        print(f"Nueva planta reproducida en zona {i}. Total: {self.plantas_por_zona[i]}")
                        return Planta(nuevo_x, nuevo_y, i, self.tipo)
                    else:
                        print(f"No se puede reproducir en zona {i}: límite alcanzado")
        return None

    def mostrar_mensaje_puntos(self):
        self.mensaje_puntos = "+100"
        self.tiempo_mensaje = pygame.time.get_ticks()

    def esta_lista(self):
        return self.estado == len(self.sprites) - 1

    def draw(self, surface):
        if not self.visible:
            return
            
        # Dibujar mensaje de puntos si existe
        if self.mensaje_puntos:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_mensaje < 3000:  # Mostrar por 3 segundos
                font = pygame.font.Font(None, 36)
                texto = font.render(self.mensaje_puntos, True, (0, 255, 0))
                pos_x = self.rect.centerx - texto.get_width() // 2
                pos_y = self.rect.top - 20
                surface.blit(texto, (pos_x, pos_y))
            else:
                self.mensaje_puntos = None
            
        

        # Dibujar el sprite de la planta correspondiente al estado actual
        if self.sprites and 0 <= self.estado < len(self.sprites):
            sprite_actual = self.sprites[self.estado]
            # Calculamos el centro exacto y ajustamos la posición vertical
            pos_x = self.rect.x + (self.rect.width - sprite_actual.get_width()) // 2 + 40
            pos_y = self.rect.y + (self.rect.height - sprite_actual.get_height()) // 2 + 35
            surface.blit(sprite_actual, (pos_x, pos_y))
            
            # Solo dibujamos detalles adicionales si es necesario
            if self.estado > 0 and self.usar_rectangulos:  # Si ya no es semilla y estamos en modo respaldo
                # Dibujar tallo principal
                tallo_rect = pygame.Rect(
                    self.rect.centerx - 2,
                    self.rect.centery,
                    4,
                    self.rect.height // 2
                )
                pygame.draw.rect(surface, self.color_tallo, tallo_rect)
                
                if self.estado == 1:  # Planta en crecimiento
                    # Dibujar hojas pequeñas
                    for i in range(2):
                        start_pos = (self.rect.centerx, self.rect.centery + i * 10)
                        end_pos_left = (start_pos[0] - 15, start_pos[1] - 5)
                        end_pos_right = (start_pos[0] + 15, start_pos[1] - 5)
                        pygame.draw.line(surface, self.color_hojas, start_pos, end_pos_left, 2)
                        pygame.draw.line(surface, self.color_hojas, start_pos, end_pos_right, 2)
                
                elif self.estado == 2:  # Planta madura
                    # Dibujar hojas largas
                    for i in range(3):
                        start_pos = (self.rect.centerx, self.rect.centery + i * 8)
                        end_pos_left = (start_pos[0] - 20, start_pos[1] - 8)
                        end_pos_right = (start_pos[0] + 20, start_pos[1] - 8)
                        pygame.draw.line(surface, self.color_hojas, start_pos, end_pos_left, 3)
                        pygame.draw.line(surface, self.color_hojas, start_pos, end_pos_right, 3)
                    
                    # Dibujar granos de arroz
                    for i in range(4):
                        for j in range(2):
                            grano_x = self.rect.centerx - 10 + j * 20
                            grano_y = self.rect.centery + i * 6
                            pygame.draw.circle(surface, self.color_arroz, (grano_x, grano_y), 2)
            
        # Indicador de agua si es necesario
        if self.necesita_agua:
            agua_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(agua_icon, (0, 100, 255, 128), (10, 10), 8)
            pygame.draw.circle(agua_icon, (0, 150, 255, 128), (10, 10), 5)
            surface.blit(agua_icon, (self.rect.right - 20, self.rect.top))