import pygame
from constants import GRAY


class LifeView:
    def __init__(self, screen, zoom):
        self.screen = screen
        self.zoom = zoom
        self.cell_alpha = {}    # {(col, row): alpha}
        self.fade_speed = 0.02   # per frame decay
        self.birth_alpha = 1.0  # alpha when cell becomes alive
        self.fade_enabled = False

    
    def set_fade_enabled(self, enabled: bool):
        self.fade_enabled = enabled


    def update_fade(self, alive_cells):
        """
        Update alpha for fading cells.
        alive_cells: set of currently alive positions {(col, row), ...}
        """
        # Fade out dead cells
        to_remove = []
        for pos, alpha in self.cell_alpha.items():
            if pos not in alive_cells:
                alpha -= self.fade_speed
                if alpha <= 0:
                    to_remove.append(pos)
                else:
                    self.cell_alpha[pos] = alpha

        for pos in to_remove:
            del self.cell_alpha[pos]

        # Set new alpha for live cells
        for pos in alive_cells:
            # Snap new births to full alpha
            self.cell_alpha[pos] = self.birth_alpha


    def draw_cells(self, alive_cells, color):
        """
        Draw cells with fade effect.
        alive_cells: set of positions
        color: RGB tuple
        """
        for pos, alpha in self.cell_alpha.items():

            # If fade disabled, only draw living cells
            if not self.fade_enabled and pos not in alive_cells:
                continue


            col, row = pos
            rect = pygame.Rect(
                col * self.zoom,
                row * self.zoom,
                self.zoom,
                self.zoom
            )

            fade_color = (
                int(color[0] * alpha + GRAY[0] * (1 - alpha)),
                int(color[1] * alpha + GRAY[1] * (1 - alpha)),
                int(color[2] * alpha + GRAY[2] * (1 - alpha)),
            )

            pygame.draw.rect(
                self.screen,
                fade_color if self.fade_enabled else color,
                rect
            )


    def draw_grid(self, width, height, color, show=False):
        """Draws the grid lines on the screen."""
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


    
