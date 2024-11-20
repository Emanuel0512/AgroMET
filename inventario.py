# inventario.py
import pygame
import constantes
from weapon import Pala, WateringCan

class Inventario:
    def __init__(self, imagen_pala, imagen_regadera, imagen_bala):
        self.visible = False
        self.herramientas = {
            'pala': Pala(imagen_pala, imagen_bala),
            'regadera': WateringCan(imagen_regadera)
        }
        self.herramienta_actual = 'pala'
        self.semillas = {
            'maiz': {'cantidad': 5, 'precio': 10},
            'tomate': {'cantidad': 3, 'precio': 15},
            'zanahoria': {'cantidad': 4, 'precio': 12}
        }
        self.dinero = 100
        
    def toggle(self):
        self.visible = not self.visible
        
    def cambiar_herramienta(self, herramienta):
        if herramienta in self.herramientas:
            self.herramienta_actual = herramienta
            
    def get_herramienta_actual(self):
        return self.herramientas.get(self.herramienta_actual)
        
    def comprar_semilla(self, tipo):
        if tipo in self.semillas:
            costo = self.semillas[tipo]['precio']
            if self.dinero >= costo:
                self.dinero -= costo
                self.semillas[tipo]['cantidad'] += 1
                return True
        return False
        
    def usar_semilla(self, tipo):
        if tipo in self.semillas and self.semillas[tipo]['cantidad'] > 0:
            self.semillas[tipo]['cantidad'] -= 1
            return True
        return False
        
    def draw(self, ventana):
        # Dibujar fondo del inventario
        pygame.draw.rect(ventana, (200, 200, 200, 128), 
                        (10, 10, 200, 300))
        
        # Mostrar dinero
        font = pygame.font.Font(None, 32)
        texto_dinero = font.render(f"${self.dinero}", True, (0, 0, 0))
        ventana.blit(texto_dinero, (20, 20))
        
        # Mostrar semillas
        y = 60
        for tipo, info in self.semillas.items():
            texto = font.render(f"{tipo}: {info['cantidad']}", True, (0, 0, 0))
            ventana.blit(texto, (20, y))
            y += 30