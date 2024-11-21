import pygame
import constantes

class SistemaProgreso:
    def __init__(self):
        self.puntos = 0
        self.nivel_actual = 'Principiante'
        self.plantas_cultivadas = 0
        self.nivel_juego = 1
        self.logros = {
            'primera_planta': False,
            'diez_plantas': False,
            'maestro_riego': False
        }
        self.font = pygame.font.Font(None, 24)
        
    def agregar_puntos(self, cantidad):
        self.puntos += cantidad
        self._actualizar_nivel()
        
    def _actualizar_nivel(self):
        for nivel, puntos in constantes.PUNTOS_NIVEL.items():
            if self.puntos >= puntos:
                self.nivel_actual = nivel
        
        # Verificar si se puede avanzar al siguiente nivel del juego
        if self.nivel_juego == 1 and self.puntos >= constantes.PUNTOS_OBJETIVO_NIVEL1:
            self.nivel_juego = 2
            return True
        return False
                
    def registrar_planta_cultivada(self):
        self.plantas_cultivadas += 1
        self.agregar_puntos(constantes.PUNTOS_POR_PLANTA)  # Dar puntos por cada planta
        if self.plantas_cultivadas == 1 and not self.logros['primera_planta']:
            self.logros['primera_planta'] = True
            self.agregar_puntos(50)
        elif self.plantas_cultivadas == 10 and not self.logros['diez_plantas']:
            self.logros['diez_plantas'] = True
            self.agregar_puntos(100)
            
    def dibujar_progreso(self, surface):
        nivel_text = self.font.render(f"Nivel: {self.nivel_actual}", True, constantes.WHITE)
        puntos_text = self.font.render(f"Puntos: {self.puntos}", True, constantes.WHITE)
        plantas_text = self.font.render(f"Plantas: {self.plantas_cultivadas}", True, constantes.WHITE)
        
        surface.blit(nivel_text, (10, 10))
        surface.blit(puntos_text, (10, 40))
        surface.blit(plantas_text, (10, 70))