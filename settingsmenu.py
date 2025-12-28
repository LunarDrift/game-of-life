import pygame
from slider import SimpleSlider
from slidersetting import SliderSetting
from colorselector import ColorSelector
from constants import (
    WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, CYAN, BUTTON_LABEL_COLOR,
    BUTTON_COLOR, PANEL_COLOR, PANEL_BORDER_COLOR
)

class SettingsMenu:
    def __init__(self):
        self.open = True
        self.clicked = False
        self.button_rect = pygame.Rect(5, 5, 80, 20)
        self.panel_rect = pygame.Rect(5, 26, 178, 200)
        self.font = pygame.font.SysFont("ubuntumono", 13)

         # User-adjustable settings
        self.zoom = 10
        self.min_zoom = 5
        self.max_zoom = 20
        self.initial_cells = 50
        self.sim_speed = 30
        self.min_update_freq = 1
        self.max_update_freq = 100
        self.show_grid = False

        # Create slider instances
        self.speed_slider = SimpleSlider(
            15, 58, 160, 13,
            self.min_update_freq, self.max_update_freq
        )

        self.zoom_slider = SimpleSlider(
            15, 93, 160, 13,
            self.min_zoom, self.max_zoom
        )

        self.initial_population_slider = SimpleSlider(
            15, 128, 160, 13,
            0, 100,
            start_val=15    # Start at 15%
        )

        # Create sliders list
        self.sliders = [
            SliderSetting(
                "Simulation Speed", self.speed_slider, self.panel_rect, step=5
            ),
            SliderSetting(
                "Zoom Level", self.zoom_slider, self.panel_rect
            ),
            SliderSetting(
                "Cell Population", self.initial_population_slider, self.panel_rect, step=5
            ),
        ]

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

        self.color_selector = ColorSelector(self.color_buttons, self.font)


############################## HELPERS ##############################
# Internal methods for drawing menu components and updating settings

    def _draw_button(self, screen, rect, label=None, label_color=(0, 0, 0), color=(0, 0, 0, 180)):
        """Draw a semi-transparent button with optional label."""
        button_surf = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )
        button_surf.fill(color)  # Semi-transparent gray by default
        screen.blit(button_surf, rect.topleft)

        txt = self.font.render(label, True, label_color)
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
        panel_surf.fill(PANEL_COLOR)
        screen.blit(panel_surf, self.panel_rect.topleft)

        # Draw panel border
        pygame.draw.rect(
            screen,
            PANEL_BORDER_COLOR,
            self.panel_rect,
            2,
            border_radius=8
        )

    
    def get_speed(self):
        """Return actual ticks for simulation based on inverted slider value."""
        max_val = self.speed_slider.max_val
        min_val = self.speed_slider.min_val
        return max_val - (self.speed_slider.val - min_val)

#########################################################################

############################# EVENTS ##############################
# Handle all events related to the settings menu

    def handle_event(self, event):
        """Handle events for the settings menu."""
        # Check if the settings button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.open = not self.open
                self.clicked = True
                return

        if not self.open:
            return
        
        for slider in self.sliders:
            slider.handle_event(event)

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
        # Draw settings button
        self._draw_button(
            screen,
            self.button_rect,
            label="Settings",
            label_color=BUTTON_LABEL_COLOR,
            color=BUTTON_COLOR
        )

        if not self.open:
            return
        
        # Draw panel background/border, sliders, color buttons
        self._draw_panel(screen)
        for slider in self.sliders:
            slider.draw(screen)
        self.color_selector.draw(screen, self.panel_rect)