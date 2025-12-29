import pygame
from constants import GRAY


class LifeView:
    def __init__(self, screen, zoom):
        # -------------------------------------------------
        # View attributes
        # -------------------------------------------------
        self.screen = screen
        self.zoom = zoom
        self.cell_fade = {}    # {(col, row): remaining_time}
        # -------------------------------------------------
        # Fade attributes
        # -------------------------------------------------
        self.fade_enabled = False
        self.prev_alive_cells = set()
        self.fade_duration = 0.5   # seconds

    
    def set_fade_enabled(self, enabled: bool):
        self.fade_enabled = enabled


    def update_fade(self, alive_cells, dt):
        """
        Update alpha for fading cells.

        :alive_cells: set of currently alive positions {(col, row), ...}
        :dt: time delta since last update in seconds
        """
        if not self.fade_enabled:
            self.cell_fade.clear()

        # Add newly dead cells to fade map
        for pos in list(self.cell_fade.keys()):
            self.cell_fade[pos] -= dt
            if self.cell_fade[pos] <= 0:
                del self.cell_fade[pos]

        # Detect deaths (cells that were alive last frame but aren't now)
        for pos in self.prev_alive_cells - alive_cells:
            self.cell_fade[pos] = self.fade_duration

        self.prev_alive_cells = set(alive_cells)

        # Set new alpha for live cells
        for pos in alive_cells:
            # Snap new births to full alpha
            self.cell_fade[pos] = self.fade_duration


    def draw_cells(self, alive_cells, color):
        """
        Draw cells with fade effect.

        :alive_cells: set of positions
        :color: RGB tuple
        """
        for pos, remaining in self.cell_fade.items():
            if not self.fade_enabled and pos not in alive_cells:
                continue

            col, row = pos
            rect = pygame.Rect(
                col * self.zoom,
                row * self.zoom,
                self.zoom,
                self.zoom
            )

            alpha = min(1.0, remaining / self.fade_duration)

            fade_color = (
                int(color[0] * alpha + GRAY[0] * (1 - alpha)),
                int(color[1] * alpha + GRAY[1] * (1 - alpha)),
                int(color[2] * alpha + GRAY[2] * (1 - alpha)),
            )

            draw_color = fade_color if self.fade_enabled else color
            pygame.draw.rect(self.screen, draw_color, rect)


    def draw_grid(self, width, height, color, show=False):
        """Draws the grid lines on the screen.

        :width: number of columns
        :height: number of rows
        :color: RGB tuple for grid line color
        :show: boolean to toggle grid visibility
        """
        if show:
            for x in range(width):
                pygame.draw.line(
                    self.screen,
                    color,
                    (x * self.zoom, 0),
                    (x * self.zoom, height * self.zoom)
                )
            for y in range(height):
                pygame.draw.line(
                    self.screen,
                    color,
                    (0, y * self.zoom),
                    (width * self.zoom, y * self.zoom)
                )