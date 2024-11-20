import pygame
from pygame.sprite import Sprite
import constantes

class NPC(Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dialogo_actual = 0
        self.tutoriales = {
            'basico': [
                "¡Bienvenido a la granja educativa!",
                "Soy tu tutor en este viaje de aprendizaje.",
                "Aprenderás sobre agricultura sostenible.",
                "Usa WASD para moverte.",
                "Presiona 1 para la pala, 2 para la regadera.",
                "¡Empecemos a cultivar!"
            ],
            'cultivo': [
                "Cada planta necesita cuidados específicos.",
                f"La temperatura óptima del arroz es {constantes.INFO_CULTIVOS['arroz']['temp_optima']}",
                "Riega las plantas cuando veas el borde azul.",
                "El tiempo entre riegos es importante.",
                "Observa los cambios en tus cultivos.",
                "¡La paciencia es clave en la agricultura!"
            ],
            'consejos_avanzados': [
                "La rotación de cultivos es importante.",
                "Mantén el suelo saludable.",
                "Observa el clima y las estaciones.",
                "Aprende sobre plagas y enfermedades.",
                "La agricultura sostenible cuida el medio ambiente."
            ],
            'consejos': constantes.INFO_CULTIVOS['arroz']['consejos']
        }
        self.tutorial_actual = 'basico'
        self.experiencia_jugador = 0
        
    def obtener_siguiente_dialogo(self):
        if self.tutorial_actual in self.tutoriales:
            if self.dialogo_actual < len(self.tutoriales[self.tutorial_actual]):
                mensaje = self.tutoriales[self.tutorial_actual][self.dialogo_actual]
                self.dialogo_actual += 1
                return mensaje
            else:
                self.dialogo_actual = 0
                return None
        return None

    def cambiar_tutorial(self, nuevo_tutorial):
        if nuevo_tutorial in self.tutoriales:
            self.tutorial_actual = nuevo_tutorial
            self.dialogo_actual = 0
            
    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)