import pygame
import json
from constants import (
    WHITE,
    PANEL_COLOR,
    PANEL_BORDER_COLOR,
    BUTTON_LABEL_COLOR,
    BUTTON_COLOR,
)


class PatternMenu:
    """Menu displaying predefined patterns with toggle button."""

    def __init__(self, json_path="patterns.json"):
        self.open = False
        # Controls button and panel rectangles
        self.button_rect = pygame.Rect(175, 5, 80, 20)
        self.panel_rect = pygame.Rect(175, 26, 200, 235)
        # Font for button labels
        self.font = pygame.font.SysFont("ubuntumono", 13)
        # Currently selected pattern
        self.selected_pattern = None
        self.pattern_buttons = []

        # Load pattern data from JSON
        with open(json_path, "r") as f:
            self.categories = json.load(f)

    def _draw_pattern_button(self, screen, rect, label):
        """Draw a button for a predefined pattern."""
        y = self.panel_rect.y + 5

        for category in self.categories:
            # Draw category title
            title_txt = self.font.render(category["name"], True, WHITE)
            screen.blit(
                title_txt, (self.panel_rect.centerx - title_txt.get_width() // 2, y)
            )
            y += 25

            for pattern in category["patterns"]:
                button_rect = pygame.Rect(
                    self.panel_rect.x + 20, y, self.panel_rect.width - 40, 20
                )
                self._draw_button(
                    screen,
                    button_rect,
                    label=pattern["label"],
                    label_color=BUTTON_LABEL_COLOR,
                    color=BUTTON_COLOR,
                )
                self.pattern_buttons.append((button_rect, pattern))
                y += 25

    def _draw_button(
        self,
        screen,
        rect,
        label=None,
        label_color=(0, 0, 0),
        color=(120, 120, 120, 100),
    ):
        """Draw a semi-transparent button with optional label."""
        button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        button_surf.fill(color)  # Semi-transparent gray by default
        screen.blit(button_surf, rect.topleft)

        txt = self.font.render(label, True, label_color)
        screen.blit(txt, txt.get_rect(center=rect.center))

    def _draw_panel(self, screen):
        """Draw the main controls panel background and border."""
        panel_surf = pygame.Surface(
            (self.panel_rect.width, self.panel_rect.height), pygame.SRCALPHA
        )
        panel_surf.fill(PANEL_COLOR)  # Semi-transparent dark gray
        screen.blit(panel_surf, self.panel_rect.topleft)

        # Draw panel border
        pygame.draw.rect(
            screen, PANEL_BORDER_COLOR, self.panel_rect, 2, border_radius=8
        )

    def handle_event(self, event):
        # Toggle menu open/close on button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.open = not self.open

        # Close menu if clicking outside panel when open
        if self.open and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.panel_rect.collidepoint(
                event.pos
            ) and not self.button_rect.collidepoint(event.pos):
                self.open = False

        # Handle pattern button clicks
        if not self.open:
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        for button_rect, pattern in self.pattern_buttons:
            if button_rect.collidepoint(event.pos):
                self.selected_pattern = pattern["file"]
                break

    def draw(self, screen):
        # Draw semi-transparent Controls button
        self._draw_button(
            screen,
            self.button_rect,
            label="Patterns",
            label_color=BUTTON_LABEL_COLOR,
            color=BUTTON_COLOR,
        )

        # if the menu is closed, no need to draw the panel
        if not self.open:
            return

        # Draw semi-transparent controls panel
        self._draw_panel(screen)

        # Draw buttons for predefined patterns
        self.pattern_buttons.clear()
        self._draw_pattern_button(screen, self.panel_rect, "Pattern")

