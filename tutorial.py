import pygame
import constantes

class SistemaTutorial:
    def __init__(self):
        self.tutorial_activo = True
        self.paso_actual = 0
        self.pasos_tutorial = [
            "¡Bienvenido a la Granja Educativa!",
            "Usa las teclas WASD para moverte",
            "Presiona 1 para seleccionar la pala",
            "Presiona 2 para seleccionar la regadera",
            "Acércate a las zonas marrones para cultivar",
            "¡Aprende mientras cultivas!"
        ]
        self.font = pygame.font.Font(None, 32)
        self.completado = False

    def mostrar_tutorial(self, ventana):
        if self.tutorial_activo and not self.completado:
            mensaje = self.pasos_tutorial[self.paso_actual]
            texto = self.font.render(mensaje, True, constantes.WHITE)
            fondo = pygame.Surface((texto.get_width() + 20, texto.get_height() + 20))
            fondo.fill(constantes.BLACK)
            fondo.set_alpha(200)
            
            pos_x = (constantes.ANCHO_VENTANA - fondo.get_width()) // 2
            pos_y = constantes.ALTO_VENTANA - 100
            
            ventana.blit(fondo, (pos_x, pos_y))
            ventana.blit(texto, (pos_x + 10, pos_y + 10))

    def siguiente_paso(self):
        if self.paso_actual < len(self.pasos_tutorial) - 1:
            self.paso_actual += 1
        else:
            self.completado = True
            self.tutorial_activo = False

    def reiniciar_tutorial(self):
        self.tutorial_activo = True
        self.paso_actual = 0
        self.completado = False
