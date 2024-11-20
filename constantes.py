import pygame

# PERSONAJE
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
SCALA_PERSONAJE = 0.4
SCALA_WATERING_CAN = 0.15
SCALA_HERRAMIENTA = 0.7
SECALA_HUECO = 0.8

# COLORES
PERSONAJE_AMARILLO = (255, 255, 0)
COLOR_HERRAMIENTA = (255, 0, 0)
COLOR_ZONA_CULTIVO = (165, 50, 0)
COLOR_BG = (0, 0, 20)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
AQUA = (0,255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (250, 0 ,0)
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)

# VELOCIDAD
FPS = 60
VELOCIDAD = 3 
VELOCIDAD_BALA = 10
VELOCIDAD_BALAS = 200

# NPC
SCALA_NPC = 1.4
VELOCIDAD_NPC = 0

# CULTIVO
MAX_HUECOS_POR_ZONA = 4
TIEMPO_CAMBIO_FASE = 10000  # 10 segundos en milisegundos
ZONAS_CULTIVO = [
    pygame.Rect(170, 400, 100, 100),  # Zona inferior izquierda
    pygame.Rect(400, 100, 200, 100),  # Zona inferior derecha
    pygame.Rect(200, 20, 200, 100)   # Zona central
]

TAMANO_PLANTA = 45
GRID_SIZE = TAMANO_PLANTA  # Para alinear los huecos en una cuadrícula
TIEMPO_CRECIMIENTO = 7000

# Información educativa de cultivos
INFO_CULTIVOS = {
    'arroz': {
        'nombre': 'Arroz',
        'tiempo_crecimiento': 10000,
        'agua_necesaria': 3,
        'temp_optima': '20-35°C',
        'info': 'El arroz es uno de los cereales más importantes del mundo.',
        'detalles': '''
            - Necesita suelos inundados
            - Clima tropical o subtropical
            - Rico en carbohidratos y proteínas
            - Principal alimento para más de la mitad de la población mundial
        ''',
        'consejos': [
            'Mantén el suelo inundado constantemente',
            'Controla las malezas manualmente',
            'Revisa el pH del suelo (ideal 6.0-7.0)',
            'Asegura buena nivelación del terreno',
            'Fertiliza con nitrógeno en las etapas clave'
        ],
        'fases': [
            'Germinación (5-10 días)',
            'Desarrollo vegetativo (25-35 días)',
            'Floración (35 días)',
            'Maduración (30-40 días)'
        ]
    },
    'maíz': {
        'nombre': 'Maíz',
        'tiempo_crecimiento': 12000,
        'agua_necesaria': 2,
        'temp_optima': '20-30°C',
        'info': 'El maíz requiere suelos ricos en nutrientes.',
        'consejos': [
            'Riega regularmente',
            'Fertiliza adecuadamente',
            'Protege del viento fuerte'
        ]
    },
    'tomate': {
        'nombre': 'Tomate',
        'tiempo_crecimiento': 15000,
        'agua_necesaria': 2,
        'temp_optima': '18-25°C',
        'info': 'Los tomates necesitan soporte para crecer.',
        'consejos': [
            'Poda los brotes laterales',
            'Riega la base de la planta',
            'Protege de heladas'
        ]
    }
}

# Niveles de aprendizaje
NIVELES_APRENDIZAJE = [
    'Principiante',
    'Agricultor Novato',
    'Agricultor Experto',
    'Maestro Agricultor'
]

# Puntos necesarios para subir de nivel
PUNTOS_NIVEL = {
    'Principiante': 0,
    'Agricultor Novato': 100,
    'Agricultor Experimentado': 300,
    'Maestro Agricultor': 600
}