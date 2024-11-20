import pygame

class PlantDetailsWindow:
    def __init__(self, plant):
        self.plant = plant
        self.window_width = 400
        self.window_height = 300
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.window_x = (screen_width - self.window_width) // 2
        self.window_y = (screen_height - self.window_height) // 2
        
        # Create a transparent surface for the window
        self.window = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        self.alpha = 0
        self.fade_speed = 10
        self.is_fading_in = True
        
        # Create a rect for checking if clicks are inside/outside the window
        self.rect = pygame.Rect(self.window_x, self.window_y, self.window_width, self.window_height)

    def run(self, main_surface):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.rect.collidepoint(mouse_pos):
                        self.is_fading_in = False
                
            # Handle fading
            if self.is_fading_in and self.alpha < 255:
                self.alpha += self.fade_speed
                if self.alpha >= 255:
                    self.alpha = 255
            elif not self.is_fading_in and self.alpha > 0:
                self.alpha -= self.fade_speed
                if self.alpha <= 0:
                    self.alpha = 0
                    running = False
            
            # Draw the window
            self.window.fill((0, 0, 0, 0))  # Clear with transparent background
            self.draw_window_background()
            self.draw_plant_details()
            
            # Apply alpha to the entire window
            self.window.set_alpha(self.alpha)
            
            # Draw the game behind the window
            main_surface.blit(self.window, (self.window_x, self.window_y))
            pygame.display.flip()

    def draw_window_background(self):
        # Draw semi-transparent background
        background = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        background.fill((50, 50, 50, 200))
        self.window.blit(background, (0, 0))
        
        # Draw border
        pygame.draw.rect(self.window, (255, 255, 255, self.alpha), 
                        (0, 0, self.window_width, self.window_height), 2)

    def draw_plant_details(self):
        # Title
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # Plant name
        title = font_large.render(self.plant.tipo.capitalize(), True, (255, 255, 255))
        title_rect = title.get_rect(centerx=self.window_width//2, y=20)
        self.window.blit(title, title_rect)
        
        # Plant info
        info_text = [
            f"Estado: {['Semilla', 'Crecimiento', 'Maduro'][self.plant.estado]}",
            f"Salud: {self.plant.salud}%",
            f"Necesita agua: {'Sí' if self.plant.necesita_agua else 'No'}",
            f"Veces regada: {self.plant.veces_regada}"
        ]
        
        y_offset = 100
        for text in info_text:
            info_surface = font_small.render(text, True, (255, 255, 255))
            info_rect = info_surface.get_rect(x=30, y=y_offset)
            self.window.blit(info_surface, info_rect)
            y_offset += 50
