import pygame
import json

class SistemaLogros:
    def __init__(self):
        self.logros = {
            'primer_cultivo': {
                'nombre': 'Primera Siembra',
                'descripcion': '¡Has plantado tu primer cultivo!',
                'completado': False
            },
            'maestro_riego': {
                'nombre': 'Maestro del Riego',
                'descripcion': 'Riega 10 plantas en el momento correcto',
                'progreso': 0,
                'meta': 10,
                'completado': False
            },
            'cosecha_perfecta': {
                'nombre': 'Cosecha Perfecta',
                'descripcion': 'Obtén una cosecha con 100% de salud',
                'completado': False
            },
            'agricultor_experto': {
                'nombre': 'Agricultor Experto',
                'descripcion': 'Completa todos los cultivos disponibles',
                'progreso': 0,
                'meta': 3,
                'completado': False
            }
        }
        
    def verificar_logro(self, tipo, valor=None):
        if tipo == 'primer_cultivo' and not self.logros['primer_cultivo']['completado']:
            self.logros['primer_cultivo']['completado'] = True
            return self.logros['primer_cultivo']
            
        elif tipo == 'maestro_riego' and not self.logros['maestro_riego']['completado']:
            self.logros['maestro_riego']['progreso'] += 1
            if self.logros['maestro_riego']['progreso'] >= self.logros['maestro_riego']['meta']:
                self.logros['maestro_riego']['completado'] = True
                return self.logros['maestro_riego']
                
        elif tipo == 'cosecha_perfecta' and valor == 100 and not self.logros['cosecha_perfecta']['completado']:
            self.logros['cosecha_perfecta']['completado'] = True
            return self.logros['cosecha_perfecta']
            
        return None
        
    def mostrar_logro(self, ventana, logro):
        # Crear superficie semitransparente para el fondo
        fondo = pygame.Surface((400, 100))
        fondo.fill((0, 0, 0))
        fondo.set_alpha(200)
        
        # Posicionar en la parte superior de la pantalla
        pos_x = (800 - 400) // 2  # Centrado horizontalmente
        pos_y = 50
        
        ventana.blit(fondo, (pos_x, pos_y))
        
        # Renderizar texto del logro
        font = pygame.font.Font(None, 32)
        titulo = font.render(f"¡Logro Desbloqueado!", True, (255, 215, 0))
        nombre = font.render(logro['nombre'], True, (255, 255, 255))
        desc = pygame.font.Font(None, 24).render(logro['descripcion'], True, (200, 200, 200))
        
        # Mostrar textos
        ventana.blit(titulo, (pos_x + 20, pos_y + 10))
        ventana.blit(nombre, (pos_x + 20, pos_y + 40))
        ventana.blit(desc, (pos_x + 20, pos_y + 70))
