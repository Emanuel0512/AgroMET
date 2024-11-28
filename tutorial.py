import pygame

class SistemaTutorial:
    def __init__(self):
        self.tutorial_texto = [
            "¡Bienvenido al juego!",
            "Controles:",
            "W - Mover arriba",
            "S - Mover abajo",
            "A - Mover izquierda",
            "D - Mover derecha",
            "1 - Usar pala",
            "2 - Usar regadera",
            "3 - Usar hoz",
            "Espacio - Interactuar",
            "Haz clic izquierdo para crear huecos.",
            "Haz clic derecho para plantar o recolectar.",
            "¡Buena suerte!"
        ]
        self.font = pygame.font.Font(None, 36)
        self.visible = True  # Al iniciar, el tutorial es visible
        self.paso_actual = 0  # Para controlar el paso actual del tutorial

    def dibujar(self, ventana):
        if not self.visible:
            return
        
        # Crear fondo semitransparente
        fondo = pygame.Surface((650, 550))
        fondo.fill((0, 0, 0))
        fondo.set_alpha(200)  # Transparente

        ventana.blit(fondo, (90, 20))  # Posicionar en el centro

        # Dibujar texto
        y_offset = 20
        for linea in self.tutorial_texto:
            texto = self.font.render(linea, True, (255, 255, 255))
            ventana.blit(texto, (200, 50 + y_offset))  # Ajustar la posición
            y_offset += 30

    def ocultar(self):
        self.visible = False