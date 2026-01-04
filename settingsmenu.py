import pygame
from slider import SimpleSlider
from slidersetting import SliderSetting
from colorselector import ColorSelector
from togglebutton import ToggleButton
from constants import (
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    BLUE,
    PURPLE,
    CYAN,
    BUTTON_LABEL_COLOR,
    BUTTON_COLOR,
    PANEL_COLOR,
    PANEL_BORDER_COLOR,
)


class SettingsMenu:
    def __init__(self):
        self.open = True
        self.clicked = False

        # -------------------------------------------------
        # Panel + button
        # -------------------------------------------------
        self.button_rect = pygame.Rect(5, 2, 80, 20)
        self.panel_rect = pygame.Rect(5, 23, 178, 255)
        self.font = pygame.font.SysFont("ubuntumono", 13)

        # -------------------------------------------------
        # User-adjustable settings
        # -------------------------------------------------
        self.zoom = 10
        self.min_zoom = 5
        self.max_zoom = 20

        self.sim_speed = 30
        self.min_update_freq = 1
        self.max_update_freq = 100

        self.initial_cells = 15
        self.show_grid = False

        self.fade_duration = 0.5
        self.min_fade_duration = 0.1
        self.max_fade_duration = 2.0

        # -------------------------------------------------
        # Cell fade button
        # -------------------------------------------------
        self.fade_toggle = ToggleButton(
            pygame.Rect(15, 147, 160, 20), "Cell Fade", value=False, font=self.font
        )
        self.fade_enabled = False

        # -------------------------------------------------
        # Sliders
        # -------------------------------------------------
        SLIDER_X = 15
        SLIDER_WIDTH = 160
        SLIDER_H = 13
        SLIDER_SPACING = 35
        y = 50

        self.speed_slider = SimpleSlider(
            SLIDER_X,
            y,
            SLIDER_WIDTH,
            SLIDER_H,
            self.min_update_freq,
            self.max_update_freq,
        )
        y += SLIDER_SPACING

        self.zoom_slider = SimpleSlider(
            SLIDER_X, y, SLIDER_WIDTH, SLIDER_H, self.min_zoom, self.max_zoom
        )
        y += SLIDER_SPACING
        self.initial_population_slider = SimpleSlider(
            SLIDER_X, y, SLIDER_WIDTH, SLIDER_H, 0, 100, start_val=15
        )
        y += SLIDER_SPACING + 35  # Extra spacing to go below toggle button
        self.fade_slider = SimpleSlider(
            SLIDER_X,
            y,
            SLIDER_WIDTH,
            SLIDER_H,
            self.min_fade_duration,
            self.max_fade_duration,
            start_val=self.fade_duration,
        )
        y += SLIDER_SPACING

        # -------------------------------------------------
        # Slider configurations for easier management
        # -------------------------------------------------
        slider_configs = [
            {
                "label": "Simulation Speed",
                "slider": self.speed_slider,
                "step": 5,
                "display_value_fn": lambda val: max(1, round(val / 2)),
            },
            {"label": "Zoom Level", "slider": self.zoom_slider},
            {
                "label": "Cell Population",
                "slider": self.initial_population_slider,
                "step": 5,
            },
            {
                "label": "Fade Time (s)",
                "slider": self.fade_slider,
                "step": 0.05,
                "display_value_fn": lambda v: f"{v:.2f}",
            },
        ]

        # -------------------------------------------------
        # Create SliderSetting instances
        # -------------------------------------------------
        self.sliders = [self._make_slider(**config) for config in slider_configs]

        # -------------------------------------------------
        # Color buttons
        # -------------------------------------------------
        BUTTON_SIZE = 20
        BUTTON_SPACING = 3

        color_y = self.panel_rect.bottom - BUTTON_SIZE * 2 - 7
        top_row = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, CYAN]
        bottom_row = [
            "darkcyan",
            "darkslategray",
            "indigo",
            "lightseagreen",
            "steelblue",
            "thistle",
            "tan",
        ]
        bottom_row = [pygame.Color(c) for c in bottom_row]

        self.color_buttons = []
        for i, color in enumerate(top_row):
            x = 15 + i * (BUTTON_SIZE + BUTTON_SPACING)
            self.color_buttons.append(
                (pygame.Rect(x, color_y, BUTTON_SIZE, BUTTON_SIZE), color)
            )

        color_y = self.panel_rect.bottom - BUTTON_SIZE - 5

        for i, color in enumerate(bottom_row):
            x = 15 + i * (BUTTON_SIZE + BUTTON_SPACING)
            self.color_buttons.append(
                (pygame.Rect(x, color_y, BUTTON_SIZE, BUTTON_SIZE), color)
            )

        self.color_selector = ColorSelector(self.color_buttons, self.font)

    ############################## HELPERS ##############################
    # Internal methods for drawing menu components and updating settings

    def _draw_soft_separator(self, screen, y):
        pygame.draw.line(
            screen,
            (200, 200, 200, 40),
            (self.panel_rect.left + 10, y),
            (self.panel_rect.right - 10, y),
        )
        pygame.draw.line(
            screen,
            (40, 40, 40, 80),
            (self.panel_rect.left + 10, y + 1),
            (self.panel_rect.right - 10, y + 1),
        )

    def _draw_separator(self, screen, y, padding=10, color=(0, 0, 0), alpha=80):
        line_surf = pygame.Surface(
            (self.panel_rect.width - padding * 2, 1), pygame.SRCALPHA
        )
        line_surf.fill((*color, alpha))
        screen.blit(line_surf, (self.panel_rect.left + padding, y))

    def _make_slider(self, label, slider, step=1, display_value_fn=None):
        return SliderSetting(
            label, slider, self.panel_rect, step=step, display_value_fn=display_value_fn
        )

    def _draw_button(
        self, screen, rect, label=None, label_color=(0, 0, 0), color=(0, 0, 0, 180)
    ):
        """Draw a semi-transparent button with optional label."""
        button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        button_surf.fill(color)  # Semi-transparent gray by default
        screen.blit(button_surf, rect.topleft)

        txt = self.font.render(label, True, label_color)
        screen.blit(txt, txt.get_rect(center=rect.center))

    def _draw_panel(self, screen):
        """Draw the main settings panel background and border."""
        panel_surf = pygame.Surface(
            (self.panel_rect.width, self.panel_rect.height), pygame.SRCALPHA
        )
        panel_surf.fill(PANEL_COLOR)
        screen.blit(panel_surf, self.panel_rect.topleft)

        # Draw panel border
        pygame.draw.rect(
            screen, PANEL_BORDER_COLOR, self.panel_rect, 2, border_radius=8
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

        if self.fade_toggle.handle_event(event):
            self.fade_enabled = self.fade_toggle.value

        for slider in self.sliders:
            slider.handle_event(event)

        # Read slider values AFTER handling events
        self.sim_speed = max(0.5, self.speed_slider.val)
        self.zoom = round(self.zoom_slider.val)
        self.initial_cells = round(self.initial_population_slider.val)
        self.fade_duration = round(self.fade_slider.val, 2)

        # Close menu if clicking outside panel
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.panel_rect.collidepoint(
                event.pos
            ) and not self.button_rect.collidepoint(event.pos):
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
            color=BUTTON_COLOR,
        )

        if not self.open:
            return

        # Draw panel background/border, sliders, color buttons
        self._draw_panel(screen)
        for slider in self.sliders:
            slider.draw(screen)

        # self._draw_separator(screen, y=140)
        self._draw_soft_separator(screen, 140)

        # Draw Cell fade toggle button
        self.fade_toggle.draw(screen)

        # self._draw_separator(screen, y=211)
        self._draw_soft_separator(screen, 211)

        self.color_selector.draw(screen, self.panel_rect)
