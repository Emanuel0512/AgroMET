
import pygame
import constantes
from personaje import Personaje
from weapon import Pala
from weapon import WateringCan
from NPC import NPC
from planta import Planta
from plant_details_window import PlantDetailsWindow
import sys
from inventario import Inventario
from clima import SistemaClima
from clima import SistemaClima
from progreso import SistemaProgreso
from tutorial import SistemaTutorial
from logros import SistemaLogros

pygame.init()

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("AgroMET")

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w * scale, h * scale))
    return nueva_imagen

def cargar_y_escalar_imagen_tierra(ruta_imagen, zonas_cultivo):
    imagen_tierra = pygame.image.load(ruta_imagen).convert_alpha()
    
    # Escalar la imagen de tierra para que cubra las zonas de cultivo
    ancho_maximo = max(zona.width for zona in zonas_cultivo)
    alto_maximo = max(zona.height for zona in zonas_cultivo)
    imagen_tierra = pygame.transform.scale(imagen_tierra, (ancho_maximo, alto_maximo))
    
    return imagen_tierra

def cargar_imagenes(nivel=1):
    animaciones = []
    for i in range(4):
        img = pygame.image.load(f"assets//image//characters//player//player_{i}.png").convert_alpha()
        img = escalar_img(img, constantes.SCALA_PERSONAJE)
        animaciones.append(img)

    imagen_pala = pygame.image.load(f"assets//image//weapons//pala.png").convert_alpha()
    imagen_pala = escalar_img(imagen_pala, constantes.SCALA_HERRAMIENTA)

    imagen_bala = pygame.image.load(f"assets//image//weapons//pala.png").convert_alpha()
    imagen_bala = escalar_img(imagen_bala, constantes.SCALA_HERRAMIENTA)

    imagen_npc = pygame.image.load(f"assets//image//npc//NPC.png").convert_alpha()
    imagen_npc = escalar_img(imagen_npc, constantes.SCALA_NPC)

    imagen_hueco = pygame.image.load(f"assets//image//hueco.png").convert_alpha()
    imagen_hueco = escalar_img(imagen_hueco, constantes.SECALA_HUECO)

    # Cargar fondo según el nivel
    fondo_path = "assets//image//mapa//fondo.jpg" if nivel == 1 else "assets//image//mapa//fondo_2.jpg"
    imagen_fondo = pygame.image.load(fondo_path).convert()
    imagen_fondo = pygame.transform.scale(imagen_fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

    imagen_watering_can = pygame.image.load(f"assets//image//watering can.png").convert_alpha()
    imagen_watering_can = escalar_img(imagen_watering_can, constantes.SCALA_WATERING_CAN)

    imagen_hoz = pygame.image.load("assets//image//hoz.png").convert_alpha()
    imagen_hoz = escalar_img(imagen_hoz, constantes.SCALA_HERRAMIENTA)

    return animaciones, imagen_pala, imagen_bala, imagen_npc, imagen_hueco, imagen_fondo, imagen_watering_can, imagen_hoz

def dibujar_zonas_cultivo(ventana, zonas_cultivo, imagen_tierra):
    for zona in zonas_cultivo:
        ventana.blit(imagen_tierra, zona)
        #pygame.draw.rect(ventana, constantes.COLOR_ZONA_CULTIVO, zona, 2)

def check_proximity(personaje, npc):
    return personaje.forma.colliderect(npc.rect)

def mostrar_nombre(ventana, nombre, x, y, color_texto):
    fuente = pygame.font.Font(None, 24)
    texto = fuente.render(nombre, True, color_texto)
    texto_rect = texto.get_rect(center=(x, y))
    ventana.blit(texto, texto_rect)

def mostrar_mensaje_con_fondo_texto(ventana, mensaje, x, y, color_texto, color_fondo):
    fuente = pygame.font.Font(None, 20)
    texto = fuente.render(mensaje, True, color_texto)
    texto_rect = texto.get_rect()
    texto_rect.topleft = (x, y)

    padding = 10
    rect_fondo = pygame.Rect(texto_rect.left - padding, texto_rect.top - padding, texto_rect.width + 2 * padding, texto_rect.height + 2 * padding)

    pygame.draw.rect(ventana, color_fondo, rect_fondo)
    ventana.blit(texto, (x, y))

def crear_hueco(jugador, pos_x, pos_y, zonas_cultivo):
    for zona in zonas_cultivo:
        if zona.rect.collidepoint(pos_x, pos_y):
            if zona.puede_agregar_hueco():
                if zona.agregar_hueco(pos_x, pos_y):
                    print("Hueco creado")
                    return True
            else:
                print("Esta zona ya tiene el máximo de huecos permitidos (4)")
                return False
    print("No puedes crear un hueco aquí")
    return False

def inicializar_juego(nivel=1):
    animaciones, imagen_pala, imagen_bala, imagen_npc, imagen_hueco, imagen_fondo, imagen_watering_can, imagen_hoz = cargar_imagenes(nivel)
    zonas_cultivo = constantes.ZONAS_CULTIVO_NIVEL1 if nivel == 1 else constantes.ZONAS_CULTIVO_NIVEL2
    imagen_tierra = cargar_y_escalar_imagen_tierra("assets//image//tierra.png", zonas_cultivo)
    jugador = Personaje(constantes.ANCHO_VENTANA // 2, constantes.ALTO_VENTANA // 2, animaciones)
    npc = NPC(100, 100, imagen_npc)
    pala = Pala(imagen_pala, imagen_bala)
    inventario = Inventario(imagen_pala, imagen_watering_can, imagen_bala, imagen_hoz)
    grupo_balas = pygame.sprite.Group()
    huecos = []
    sistema_clima = SistemaClima()
    return jugador, npc, pala, grupo_balas, huecos, imagen_hueco, imagen_fondo, imagen_tierra, sistema_clima, inventario, imagen_hueco, imagen_hoz

class ZonaCultivo:
    def __init__(self, rect):
        self.rect = rect
        self.huecos = []
        self.plantas = {} 
        self.max_plantas = constantes.MAX_HUECOS_POR_ZONA

    def puede_agregar_hueco(self):
        return len(self.huecos) < constantes.MAX_HUECOS_POR_ZONA

    def agregar_hueco(self, x, y):
        if not self.puede_agregar_hueco():
            print("Máximo de huecos alcanzado")
            return False

        # Verificar si ya existe una planta en esta posición
        for planta_pos, planta in self.plantas.items():
            planta_x, planta_y = planta_pos
            if abs(planta_x - x) < constantes.TAMANO_PLANTA and abs(planta_y - y) < constantes.TAMANO_PLANTA:
                print("No se puede crear un hueco sobre una planta")
                return False

        # Calcular la posición en la cuadrícula
        rel_x = x - self.rect.x
        rel_y = y - self.rect.y
        
        # Encontrar la siguiente posición disponible en la cuadrícula
        next_pos = len(self.huecos)
        grid_row = next_pos // constantes.GRID_COLS
        grid_col = next_pos % constantes.GRID_COLS
        
        if grid_row >= constantes.GRID_ROWS:
            print("No hay más espacio en la cuadrícula")
            return False
            
        # Calcular la posición exacta del nuevo hueco
        hueco_x = self.rect.x + (grid_col * constantes.TAMANO_PLANTA)
        hueco_y = self.rect.y + (grid_row * constantes.TAMANO_PLANTA)
        
        nuevo_hueco = pygame.Rect(hueco_x, hueco_y, constantes.TAMANO_PLANTA, constantes.TAMANO_PLANTA)
        
        # Verificar si ya existe un hueco en esta posición
        for hueco in self.huecos:
            if hueco.colliderect(nuevo_hueco):
                return False
        
        self.huecos.append(nuevo_hueco)
        print(f"Hueco creado en posición [{grid_col},{grid_row}]")
        return True

    def agregar_planta(self, hueco):
        hueco_key = (hueco.x, hueco.y)
        if hueco in self.huecos and hueco_key not in self.plantas:
            nueva_planta = Planta(hueco.x, hueco.y)
            self.plantas[hueco_key] = nueva_planta
            return True
        return False

    def regar_planta(self, pos):
        for planta in self.plantas.values():
            if planta.rect.collidepoint(pos[0], pos[1]):
                return planta.regar()
        return False
    
def ejecutar_juego(ventana, jugador, inventario, npc, pala, grupo_balas, huecos, imagen_hueco, imagen_fondo, imagen_tierra, zonas_cultivo, sistema_clima, sistema_puntos, nivel=1):
    reloj = pygame.time.Clock()
    mover_arriba = mover_abajo = mover_izquierda = mover_derecha = False
    dialogo_activo = False
    indice_dialogo = 0
    turno_personaje = False
    dialogos_npc = ["¡Buenos dias¡, Parece que estas un poco perdido","Tranquilo, Mira, esta es la zona donde cultivamo el arroz","No te preocupes, Mira","yo ya me encargue de preparar la tierra cuidadosamente","ahora es tu turno","Claro!, primero caba cuatro huecos en cada una de las zonas de cultivo, y luego..","planta estas semillas de arroz en cada hueco que hiciste","No, Ahora tienes que regar cada planta poco a poco hasta que florescan","Cuando florescan, puedes recolectarlas con ese extraño objeto que tienes en tu bolsillo","y listo, estare observando desde aqui, si necesitas algo te lo repetire todo de nuevo"]
    dialogo_personaje = ["Si...No estoy seguro de que hacer, ni como ayudar aqui", "¡Oh! pero y yo como puedo ayudar? tan solo soy un niño...", "¿?", "Con mis brazos debiles no hubiera podido hacer tal cosa...","quien? yo?", "luego..."," y ya?","Asi que para eso servia esta chocolatera o regadera... o lo que sea esto","que? aaa...el cuchillo raro, no se que tine mi papa en la cabeza para darme esto...","muchas gracias Sebastian"]
    
    sistema_tutorial = SistemaTutorial()

    run = True
    while run:
        reloj.tick(constantes.FPS)
        ventana.blit(imagen_fondo, (0, 0))
   
        dibujar_zonas_cultivo(ventana, zonas_cultivo, imagen_tierra)
        
        for zona in zonas_cultivo:
            for planta in zona.plantas.values():
                resultado = planta.update()
                if resultado == "completado":
                    mostrar_mensaje_con_fondo_texto(ventana, "¡Completado!", planta.rect.centerx, planta.rect.top - 20, constantes.WHITE, constantes.GREEN)
                planta.draw(ventana)
        
        delta_x = 0
        delta_y = 0
        
        if mover_derecha: delta_x = constantes.VELOCIDAD
        if mover_izquierda: delta_x = -constantes.VELOCIDAD
        if mover_arriba: delta_y = -constantes.VELOCIDAD
        if mover_abajo: delta_y = constantes.VELOCIDAD

        jugador.movimiento(delta_x, delta_y)

        if check_proximity(jugador, npc):
            dialogo_activo = True
        else:
            dialogo_activo = False
            indice_dialogo = 0

        jugador.update()
        npc.update()
        pala.update(jugador)

        # Dibujar huecos existentes
        for zona in zonas_cultivo:
            for hueco in zona.huecos:
                ventana.blit(imagen_hueco, (hueco.x - 10, hueco.y))
        
        npc.draw(ventana)
        jugador.dibujar(ventana)

        mostrar_nombre(ventana, "Miguel", jugador.forma.centerx, jugador.forma.top - 10, constantes.AQUA)
        mostrar_nombre(ventana, "Sebastian", npc.rect.centerx, npc.rect.top - 30, constantes.LIME)

        pala.dibujar(ventana)
        
        for bala in grupo_balas:
            bala.dibujar(ventana)

        if dialogo_activo and indice_dialogo < len(dialogos_npc):
            if turno_personaje:
                mostrar_mensaje_con_fondo_texto(ventana, dialogo_personaje[indice_dialogo], jugador.forma.x + 25, jugador.forma.y + 10, constantes.WHITE, constantes.BLACK)
            else:
                mostrar_mensaje_con_fondo_texto(ventana, dialogos_npc[indice_dialogo], npc.rect.x, npc.rect.y - 10, constantes.WHITE, constantes.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if sistema_tutorial.visible:
                        sistema_tutorial.ocultar()
                if event.key == pygame.K_a: 
                    mover_izquierda = True
                    if sistema_tutorial.visible:  # Tutorial de movimiento
                        sistema_tutorial.paso_actual += 1
                if event.key == pygame.K_d: 
                    mover_derecha = True
                    if sistema_tutorial.visible:
                        sistema_tutorial.paso_actual += 1
                if event.key == pygame.K_w: 
                    mover_arriba = True
                    if sistema_tutorial.visible:
                        sistema_tutorial.paso_actual += 1  # Tutorial de movimiento
                if event.key == pygame.K_s: 
                    mover_abajo = True
                    if sistema_tutorial.visible:
                            sistema_tutorial.paso_actual += 1
                
                if event.key == pygame.K_SPACE and dialogo_activo:
                    turno_personaje = not turno_personaje
                    if not turno_personaje:
                        indice_dialogo += 1
                        if indice_dialogo >= len(dialogos_npc):
                            indice_dialogo = 0  
                    
                if event.key == pygame.K_i:
                    inventario.toggle()
                if event.key == pygame.K_1:
                    inventario.cambiar_herramienta('pala')
                if event.key == pygame.K_2:
                    inventario.cambiar_herramienta('regadera')
                if event.key == pygame.K_3:
                    inventario.cambiar_herramienta('hoz')
                if event.key == pygame.K_r and inventario.herramienta_actual == 'regadera':
                    jugador.regar()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: mover_izquierda = False
                if event.key == pygame.K_d: mover_derecha = False
                if event.key == pygame.K_w: mover_arriba = False
                if event.key == pygame.K_s: mover_abajo = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # Click izquierdo
                    # Verificar si se hizo clic en el botón Next
                    if sistema_puntos.boton_next and sistema_puntos.boton_next.collidepoint(pos):
                        sistema_puntos.nivel_actual += 1
                        # Cargar el nuevo fondo para el nivel 2
                        imagen_fondo = pygame.image.load("assets/image/mapa/fondo_2.jpg")
                        imagen_fondo = pygame.transform.scale(imagen_fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
                        sistema_puntos.puntos = 0  # Reiniciar puntos para el nuevo nivel
                        continue
                    for zona in zonas_cultivo:
                        if zona.rect.collidepoint(pos) and inventario.herramienta_actual == 'pala':
                            if len(zona.huecos) < constantes.MAX_HUECOS_POR_ZONA:
                                if zona.agregar_hueco(pos[0], pos[1]):
                                    # Dibujar el hueco inmediatamente
                                    hueco = zona.huecos[-1]  # Get the last added hole
                                    ventana.blit(imagen_hueco, (hueco.x - 15, hueco.y))
                                    pygame.display.update()
                            else:
                                print("Esta zona ya tiene el máximo de huecos permitidos")
                        elif zona.rect.collidepoint(pos) and inventario.herramienta_actual == 'regadera':
                            if zona.regar_planta(pos):
                                print("Planta regada")
                elif event.button == 3:  # Click derecho para plantar, recolectar o ver detalles
                    for zona in zonas_cultivo:
                        # Primero, verificar si hay una planta en la posición del click
                        for hueco_pos, planta in list(zona.plantas.items()):
                            if planta.rect.collidepoint(pos):
                                if inventario.herramienta_actual == 'hoz' and planta.estado == 2 and not planta.recolectada:
                                    # Recolectar la planta
                                    planta.recolectada = True
                                    sistema_puntos.agregar_puntos(constantes.PUNTOS_POR_PLANTA)  # Dar puntos por planta recolectada
                                    del zona.plantas[hueco_pos]
                                    print(f"Planta recolectada! +{constantes.PUNTOS_POR_PLANTA} puntos")
                                    if sistema_puntos.objetivo_cumplido():
                                        print("¡Felicitaciones! Has alcanzado el objetivo de puntos!")
                                else:
                                    # Mostrar detalles de la planta
                                    details_window = PlantDetailsWindow(planta)
                                    details_window.run(ventana)
                                break
                        # Si no se hizo click en una planta, intentar plantar
                        if zona.rect.collidepoint(pos):
                            # Buscar si ya existe un hueco en esa posición
                            hueco_encontrado = None
                            for hueco in zona.huecos:
                                if hueco.collidepoint(pos):
                                    hueco_encontrado = hueco
                                    break
                            
                            if hueco_encontrado:
                                # Si hay hueco, intentar plantar
                                # Verificar el límite de plantas en la zona actual
                                if len(zona.plantas) < constantes.MAX_PLANTAS_POR_ZONA:
                                    if zona.agregar_planta(hueco_encontrado):
                                        # Buscar y eliminar el hueco por posición
                                        hueco_a_eliminar = None
                                        for h in zona.huecos:
                                            if h.x == hueco_encontrado.x and h.y == hueco_encontrado.y:
                                                hueco_a_eliminar = h
                                                break
                                        if hueco_a_eliminar:
                                            zona.huecos.remove(hueco_a_eliminar)
                                            print(f"Planta cultivada en posición ({hueco_encontrado.x}, {hueco_encontrado.y})")
                                        else:
                                            print("Error: No se pudo eliminar el hueco")
                                    else:
                                        print("No se puede cultivar aquí")
                                else:
                                    print(f"Máximo de plantas alcanzado en esta zona ({constantes.MAX_PLANTAS_POR_ZONA})")
                            else:
                                print("Primero debes crear un hueco con click izquierdo")

        herramienta_actual = inventario.get_herramienta_actual()
        if herramienta_actual is not None:
            herramienta_actual.update(jugador)
            herramienta_actual.dibujar(ventana)

        if inventario.visible:
            inventario.draw(ventana)

        # Actualizar y mostrar información del clima
        sistema_clima.actualizar()
        info_clima = sistema_clima.obtener_info()
        font = pygame.font.Font(None, 24)
        texto_clima = font.render(f"Temp: {info_clima['temperatura']}°C  Humedad: {info_clima['humedad']}%  {'Lluvia' if info_clima['lluvia'] else 'Despejado'}", True, constantes.WHITE)
        ventana.blit(texto_clima, (10, constantes.ALTO_VENTANA - 30))

        # Mostrar el tutorial si está activo
        sistema_tutorial.dibujar(ventana)
        
        # Dibujar el contador de puntos
        sistema_puntos.dibujar(ventana)
        
        # Mostrar mensaje de victoria si se alcanzó el objetivo
        sistema_puntos.mostrar_mensaje_victoria(ventana)
        
        pygame.display.flip()

    return True

def mostrar_mensaje_nivel_completado(ventana):
    # Oscurecer la pantalla
    overlay = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    overlay.fill(constantes.BLACK)
    overlay.set_alpha(128)
    ventana.blit(overlay, (0, 0))
    
    # Mostrar mensaje
    font = pygame.font.Font(None, 64)
    mensaje = font.render("¡Nivel Completado!", True, constantes.WHITE)
    mensaje_rect = mensaje.get_rect(center=(constantes.ANCHO_VENTANA // 2, constantes.ALTO_VENTANA // 2))
    ventana.blit(mensaje, mensaje_rect)
    
    # Mostrar instrucción
    font_pequeño = pygame.font.Font(None, 32)
    instruccion = font_pequeño.render("Presiona ESPACIO para continuar", True, constantes.WHITE)
    instruccion_rect = instruccion.get_rect(center=(constantes.ANCHO_VENTANA // 2, mensaje_rect.bottom + 50))
    ventana.blit(instruccion, instruccion_rect)
    
    pygame.display.flip()
    
    # Esperar a que el jugador presione ESPACIO
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    esperando = False

def draw_button(screen, text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

def menu_principal(ventana):
    fondo = pygame.image.load("assets//image//menubg.jpeg")  
    fondo = pygame.transform.scale(fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    
    while True:
        ventana.blit(fondo, (0, 0))
        
        titulo_font = pygame.font.Font(None, 72)
        titulo_text = titulo_font.render("AgroMET - Juego de Granja", True, constantes.WHITE)
        titulo_rect = titulo_text.get_rect(center=(constantes.ANCHO_VENTANA // 2, 100))
        ventana.blit(titulo_text, titulo_rect)
        
        jugar_boton = draw_button(ventana, "Comenzar", constantes.ANCHO_VENTANA // 2 - 100, 300, 200, 50, constantes.GREEN, constantes.WHITE)
        salir_boton = draw_button(ventana, "Cerrar", constantes.ANCHO_VENTANA // 2 - 100, 400, 200, 50, constantes.RED, constantes.WHITE)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if jugar_boton.collidepoint(event.pos):
                    return True
                elif salir_boton.collidepoint(event.pos):
                    return False

def pantalla_carga(ventana):
    fondo = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    fondo.fill(constantes.BLACK)
    
    barra_carga = pygame.Rect(100, constantes.ALTO_VENTANA // 2 - 25, constantes.ANCHO_VENTANA - 200, 50)
    
    reloj = pygame.time.Clock()

    for i in range(101):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        ventana.blit(fondo, (0, 0))
        
        pygame.draw.rect(ventana, constantes.WHITE, barra_carga, 2)
        pygame.draw.rect(ventana, constantes.GREEN, (barra_carga.left, barra_carga.top, barra_carga.width * i // 100, barra_carga.height))
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Cargando el juego... {i}%", True, constantes.WHITE)
        text_rect = text.get_rect(center=(constantes.ANCHO_VENTANA // 2, barra_carga.bottom + 50))
        ventana.blit(text, text_rect)
        
        pygame.display.flip()

        reloj.tick(30)
    
    return True

def mostrar_menu_plantas(ventana, pos):
    # Lista de plantas disponibles
    plantas_disponibles = ["Tomate", "Zanahoria", "Lechuga", "Papa"]
    
    # Crear rectángulos para cada opción
    opciones = []
    ancho_opcion = 100
    alto_opcion = 30
    x = pos[0]
    y = pos[1]
    
    # Dibujar fondo del menú
    menu_rect = pygame.Rect(x, y, ancho_opcion, alto_opcion * len(plantas_disponibles))
    pygame.draw.rect(ventana, constantes.WHITE, menu_rect)
    pygame.draw.rect(ventana, constantes.BLACK, menu_rect, 2)
    
    # Dibujar opciones
    font = pygame.font.Font(None, 24)
    for i, planta in enumerate(plantas_disponibles):
        opcion_rect = pygame.Rect(x, y + i * alto_opcion, ancho_opcion, alto_opcion)
        pygame.draw.rect(ventana, constantes.WHITE, opcion_rect)
        pygame.draw.rect(ventana, constantes.BLACK, opcion_rect, 1)
        
        texto = font.render(planta, True, constantes.BLACK)
        texto_rect = texto.get_rect(center=opcion_rect.center)
        ventana.blit(texto, texto_rect)
        opciones.append((opcion_rect, planta))
    
    pygame.display.flip()
    
    # Esperar selección
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    mouse_pos = pygame.mouse.get_pos()
                    for rect, planta in opciones:
                        if rect.collidepoint(mouse_pos):
                            return planta
                elif event.button == 3:  # Click derecho para cancelar
                    return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para cancelar
                    return None
    
class SistemaPuntos:
    def __init__(self):
        self.puntos = 0
        self.font = pygame.font.Font(None, 36)
        self.nivel_actual = 1
        self.boton_next = None
    
    def agregar_puntos(self, cantidad):
        self.puntos += cantidad
        
    def dibujar(self, ventana):
        # Determinar el objetivo según el nivel
        objetivo = constantes.PUNTOS_OBJETIVO_NIVEL1 if self.nivel_actual == 1 else constantes.PUNTOS_OBJETIVO_NIVEL2
        
        # Crear superficie semitransparente para el fondo
        texto = self.font.render(f'Puntos: {self.puntos}/{objetivo}', True, (255, 215, 0))  # Color amarillo dorado
        fondo = pygame.Surface((texto.get_width() + 20, texto.get_height() + 20))
        fondo.fill((0, 0, 0))
        fondo.set_alpha(200)
        
        # Posicionar y dibujar el fondo y texto
        ventana.blit(fondo, (5, 5))
        ventana.blit(texto, (15, 15))
        
    def objetivo_cumplido(self):
        objetivo = constantes.PUNTOS_OBJETIVO_NIVEL1 if self.nivel_actual == 1 else constantes.PUNTOS_OBJETIVO_NIVEL2
        return self.puntos >= objetivo

    def mostrar_mensaje_victoria(self, ventana):
        if self.objetivo_cumplido():
            # Crear superficie semitransparente para el fondo
            fondo = pygame.Surface((400, 250))  # Aumentado el alto para el botón
            fondo.fill((0, 0, 0))
            fondo.set_alpha(200)
            
            # Posicionar en el centro de la pantalla
            pos_x = (constantes.ANCHO_VENTANA - 400) // 2
            pos_y = (constantes.ALTO_VENTANA - 250) // 2
            
            ventana.blit(fondo, (pos_x, pos_y))
            
            # Renderizar texto
            font = pygame.font.Font(None, 48)
            texto = font.render("¡Felicidades!", True, (255, 215, 0))
            texto2 = font.render(f"Ganaste el nivel {self.nivel_actual}", True, (255, 255, 255))
            
            # Centrar y mostrar textos
            ventana.blit(texto, (pos_x + (400 - texto.get_width()) // 2, pos_y + 50))
            ventana.blit(texto2, (pos_x + (400 - texto2.get_width()) // 2, pos_y + 100))
            
            # Crear y mostrar botón Next
            boton_width = 120
            boton_height = 40
            boton_x = pos_x + (400 - boton_width) // 2
            boton_y = pos_y + 160
            
            self.boton_next = pygame.Rect(boton_x, boton_y, boton_width, boton_height)
            pygame.draw.rect(ventana, (0, 200, 0), self.boton_next)  # Verde
            
            # Texto del botón
            font_boton = pygame.font.Font(None, 36)
            texto_boton = font_boton.render("Next", True, (255, 255, 255))
            texto_rect = texto_boton.get_rect(center=self.boton_next.center)
            ventana.blit(texto_boton, texto_rect)
            
            return True
        return False

def main():
    try:
        pygame.init()
        sistema_puntos = SistemaPuntos()
        if menu_principal(ventana):
            print("Iniciando pantalla de carga...")
         
            pygame.display.update()
            
            carga_completada = pantalla_carga(ventana)
            print(f"Pantalla de carga completada: {carga_completada}")
            
            if carga_completada:
                nivel_actual = 1
                while nivel_actual <= 2:
                    # Inicializar todos los componentes del juego para el nivel actual
                    jugador, npc, pala, grupo_balas, huecos, imagen_hueco, imagen_fondo, imagen_tierra, sistema_clima, inventario, imagen_hueco, imagen_hoz = inicializar_juego(nivel_actual)
                    zonas_cultivo = [ZonaCultivo(zona) for zona in (constantes.ZONAS_CULTIVO_NIVEL1 if nivel_actual == 1 else constantes.ZONAS_CULTIVO_NIVEL2)]
                    print(f"Iniciando nivel {nivel_actual}...")
                    
                    if ejecutar_juego(ventana, jugador, inventario, npc, pala, grupo_balas, huecos, imagen_hueco, imagen_fondo, imagen_tierra, zonas_cultivo, sistema_clima, sistema_puntos):
                        if sistema_puntos.puntos >= (constantes.PUNTOS_OBJETIVO_NIVEL1 if nivel_actual == 1 else constantes.PUNTOS_OBJETIVO_NIVEL2):
                            nivel_actual += 1
                            if nivel_actual <= 2:
                                mostrar_mensaje_nivel_completado(ventana)
                        else:
                            break
                    else:
                        break
    except Exception as e:
        print(f"Error en la ejecución del juego: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit() 
        sys.exit()

if __name__ == "__main__":
    main()