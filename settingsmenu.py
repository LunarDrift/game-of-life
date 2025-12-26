import pygame
from slider import SimpleSlider

class SettingsMenu:
    def __init__(self):
        self.open = True
        self.clicked = False

        # User-adjustable settings
        self.tile_size = 10
        self.min_tile_size = 2
        self.max_tile_size = 20
        self.initial_cells = 50
        self.sim_speed = 30
        self.min_update_freq = 1
        self.max_update_freq = 100
        self.show_grid = False

        # Settings button and panel rectangles
        self.button_rect = pygame.Rect(5, 5, 80, 20)
        self.panel_rect = pygame.Rect(5, 26, 180, 200)

        # Sliders for settings
        self.speed_slider = SimpleSlider(
            14,
            58,
            170,
            15,
            self.min_update_freq,
            self.max_update_freq
        )

        self.tile_size_slider = SimpleSlider(
            14,
            93,
            170,
            15,
            self.min_tile_size,
            self.max_tile_size
        )

        self.initial_population_slider = SimpleSlider(
            14,
            128,
            170,
            15,
            0,
            100
        )



        self.font = pygame.font.SysFont("ubuntumono", 13)


    def handle_event(self, event):
        # Check if the settings button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.open = not self.open
                self.clicked = True
                return
            
        # If menu is not open, ignore other events
        if not self.open:
            return
        
        # Always forward events to sliders when menu is open
        self.speed_slider.handle_event(event)
        self.tile_size_slider.handle_event(event)
        self.initial_population_slider.handle_event(event)

        # Read slider values AFTER handling events
        slider = self.speed_slider
        # Invert speed slider values to be more intuitive
        self.sim_speed = round(slider.max_val - (slider.val - slider.min_val))
        self.tile_size = round(self.tile_size_slider.val)
        self.initial_cells = round(self.initial_population_slider.val)

        # Close menu if clicking outside panel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                not self.panel_rect.collidepoint(event.pos)
                and not self.button_rect.collidepoint(event.pos)
            ):
                self.open = False
        
        # Release clicked state
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False


    def draw(self, screen):
        # Draw semi-transparent Settings button
        button_surf = pygame.Surface(
            (self.button_rect.width, self.button_rect.height),
            pygame.SRCALPHA
        )
        button_surf.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(button_surf, self.button_rect.topleft)

        button_txt = self.font.render("Settings", True, (255, 255, 0))
        screen.blit(
            button_txt,
            button_txt.get_rect(center=self.button_rect.center)
        )

        # if the menu is closed, no need to draw the panel
        if not self.open:
            return
        
        # Draw semi-transparent settings panel
        panel_surf = pygame.Surface(
            (self.panel_rect.width, self.panel_rect.height),
            pygame.SRCALPHA
        )
        panel_surf.fill((40, 40, 40, 150)) # Semi-transparent dark gray
        screen.blit(panel_surf, self.panel_rect.topleft)

        # Draw panel border
        pygame.draw.rect(
            screen,
            (200, 200, 0),
            self.panel_rect,
            2,
            border_radius=8
        )

        # Get surfaces for slider labels
        speed_label_surface = self.font.render(
            f"Simulation Speed: {round(self.speed_slider.val)}",
            True,
            (255, 255, 255)
        )

        tile_size_label_surface = self.font.render(
            f"Zoom Level: {round(self.tile_size_slider.val)}",
            True,
            (255, 255, 255)
        )

        percent = round(self.initial_population_slider.val)
        cell_count_label_surface = self.font.render(
            f"Initial Population: {percent}%",
            True,
            (255, 255, 255)
        )


        # Get label rects to center its x position within the panel place it above the slider
        speed_label_rect = speed_label_surface.get_rect(centerx=self.panel_rect.centerx)
        speed_label_rect.bottom = self.speed_slider.rect.top - 2
        screen.blit(speed_label_surface, speed_label_rect)

        tile_size_label_rect = tile_size_label_surface.get_rect(centerx=self.panel_rect.centerx)
        tile_size_label_rect.bottom = self.tile_size_slider.rect.top - 2
        screen.blit(tile_size_label_surface, tile_size_label_rect)

        cell_count_label_rect = cell_count_label_surface.get_rect(centerx=self.panel_rect.centerx)
        cell_count_label_rect.bottom = self.initial_population_slider.rect.top - 2
        screen.blit(cell_count_label_surface, cell_count_label_rect)


        # Draw sliders
        self.speed_slider.draw(screen)
        self.tile_size_slider.draw(screen)
        self.initial_population_slider.draw(screen)