import random
import pygame
import constantes

class SistemaClima:
    def __init__(self):
        self.temperatura = 25  # temperatura en celsius
        self.humedad = 60      # porcentaje
        self.lluvia = False
        self.ultimo_cambio = pygame.time.get_ticks()
        self.intervalo_cambio = 30000  # 30 segundos
        
    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
            self.temperatura += random.uniform(-2, 2)
            self.temperatura = max(10, min(35, self.temperatura))
            
            self.humedad += random.uniform(-5, 5)
            self.humedad = max(30, min(90, self.humedad))
            
            self.lluvia = random.random() < 0.3  # 30% de probabilidad de lluvia
            self.ultimo_cambio = tiempo_actual
            
    def obtener_info(self):
        return {
            'temperatura': round(self.temperatura, 1),
            'humedad': round(self.humedad, 1),
            'lluvia': self.lluvia
        }
    
    def afecta_cultivo(self, tipo_cultivo):
        info_cultivo = constantes.INFO_CULTIVOS[tipo_cultivo]
        temp_min, temp_max = map(int, info_cultivo['temp_optima'].replace('°C', '').split('-'))
        
        # Calcula el efecto en la salud de la planta
        efecto = 0
        if self.temperatura < temp_min:
            efecto -= (temp_min - self.temperatura) * 2
        elif self.temperatura > temp_max:
            efecto -= (self.temperatura - temp_max) * 2
            
        if self.humedad < 40:
            efecto -= (40 - self.humedad) / 2
        elif self.humedad > 80:
            efecto -= (self.humedad - 80) / 2
            
        if self.lluvia:
            efecto += 5  # La lluvia es generalmente beneficiosa
            
        return max(-10, min(10, efecto))  # Limita el efecto entre -10 y +10
