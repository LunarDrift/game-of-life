import pygame
from slider import SimpleSlider
from constants import (
    RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, CYAN
)

class SettingsMenu:
    def __init__(self):
        self.open = True
        self.clicked = False

        # User-adjustable settings
        self.zoom = 10
        self.min_zoom = 2
        self.max_zoom = 20
        self.initial_cells = 50
        self.sim_speed = 30
        self.min_update_freq = 1
        self.max_update_freq = 100
        self.show_grid = False
        self.cell_color = YELLOW

        # Settings button and panel rectangles
        self.button_rect = pygame.Rect(5, 5, 80, 20)
        self.panel_rect = pygame.Rect(5, 26, 178, 200)

        # Color button rects L, T, W, H
        self.color_buttons = [
        # Top row
            (pygame.Rect(15, 163, 20, 20), RED),
            (pygame.Rect(38, 163, 20, 20), ORANGE),
            (pygame.Rect(61, 163, 20, 20), YELLOW),
            (pygame.Rect(84, 163, 20, 20), GREEN),
            (pygame.Rect(107, 163, 20, 20), BLUE),
            (pygame.Rect(130, 163, 20, 20), PURPLE),
            (pygame.Rect(153, 163, 20, 20), CYAN),
            # Bottom row
            (pygame.Rect(15, 188, 20, 20), "darkcyan"),
            (pygame.Rect(38, 188, 20, 20), "darkslategray"),
            (pygame.Rect(61, 188, 20, 20), "indigo"),
            (pygame.Rect(84, 188, 20, 20), "lightseagreen"),
            (pygame.Rect(107, 188, 20, 20), "steelblue"),
            (pygame.Rect(130, 188, 20, 20), "thistle"),
            (pygame.Rect(153, 188, 20, 20), "tan"),
        ]


        # Sliders for settings
        self.speed_slider = SimpleSlider(
            15,
            58,
            160,
            13,
            self.min_update_freq,
            self.max_update_freq
        )

        self.zoom_slider = SimpleSlider(
            15,
            93,
            160,
            13,
            self.min_zoom,
            self.max_zoom
        )

        self.initial_population_slider = SimpleSlider(
            15,
            128,
            160,
            13,
            0,
            100,
            start_val=25    # Start at 25%
        )



        self.font = pygame.font.SysFont("ubuntumono", 13)

############################## HELPERS ##############################
# Internal methods for drawing menu components and updating settings

    def _draw_button(self, screen, rect, label=None, color=(120, 120, 120, 100)):
        """Draw a semi-transparent button with optional label."""
        button_surf = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )
        button_surf.fill(color)  # Semi-transparent gray by default
        screen.blit(button_surf, rect.topleft)

        txt = self.font.render(label, True, (0, 0, 0))
        screen.blit(
            txt,
            txt.get_rect(center=rect.center)
        )


    def _draw_panel(self, screen):
        """Draw the main settings panel background and border."""
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


    def _draw_slider_label(self, screen, slider, text, offset=-2):
        """Draw the label above a given slider."""
        label_surface = self.font.render(text, True, (255, 255, 255))
        label_rect = label_surface.get_rect(
            centerx=self.panel_rect.centerx
        )
        label_rect.bottom = slider.rect.top + offset
        screen.blit(label_surface, label_rect)


    def _draw_sliders(self, screen):
        """Draw all sliders and their labels."""
        self._draw_slider_label(
            screen, self.speed_slider, f"Simulation Speed: {round(self.speed_slider.val)}"
        )
        self._draw_slider_label(
            screen, self.zoom_slider, f"Zoom Level: {round(self.zoom_slider.val)}"
        )
        self._draw_slider_label(
            screen,
            self.initial_population_slider,
            f"Initial Population: {round(self.initial_population_slider.val)}%",
        )

        # Draw sliders themselves
        self.speed_slider.draw(screen)
        self.zoom_slider.draw(screen)
        self.initial_population_slider.draw(screen)


    def _draw_color_buttons(self, screen):
        """Draw all cell color buttons and the label."""
        color_label_surface = self.font.render(
            "Cell Colors", True, (255, 255, 255)
        )
        color_label_rect = color_label_surface.get_rect(
            centerx=self.panel_rect.centerx
        )
        color_label_rect.bottom = 160
        screen.blit(color_label_surface, color_label_rect)

        for rect, color in self.color_buttons:
            self._draw_button(screen, rect, color=color)

    
    def get_speed(self):
        """Return actual ticks for simulation based on inverted slider value."""
        max_val = self.speed_slider.max_val
        min_val = self.speed_slider.min_val
        return max_val - (self.speed_slider.val - min_val)

#########################################################################

############################# EVENTS ##############################
# Handle all events related to the settings menu

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

        # Check for color selection button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Iterate through color buttons to see if one was clicked
            for rect, color in self.color_buttons:
                if rect.collidepoint(event.pos):
                    self.cell_color = color
                    break

        # Always forward events to sliders when menu is open
        self.speed_slider.handle_event(event)
        self.zoom_slider.handle_event(event)
        self.initial_population_slider.handle_event(event)

        # Read slider values AFTER handling events
        self.sim_speed = max(0.5, self.speed_slider.val)
        self.zoom = round(self.zoom_slider.val)
        self.initial_cells = round(self.initial_population_slider.val)

        # Close menu if clicking outside panel
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (
                not self.panel_rect.collidepoint(event.pos)
                and not self.button_rect.collidepoint(event.pos)
            ):
                self.open = False
        
        # Release clicked state
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

#########################################################################

############################ DRAWING ##############################

    def draw(self, screen):
        """Draw the settings menu button and panel if open."""
        # Settings button
        self._draw_button(screen, self.button_rect, label="Settings", color=(0, 0, 0, 180))

        if not self.open:
            return
        
        # Panel + sliders + colors
        self._draw_panel(screen)
        self._draw_sliders(screen)
        self._draw_color_buttons(screen)