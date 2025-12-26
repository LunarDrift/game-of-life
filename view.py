import pygame


class LifeView:
    def __init__(self, screen, zoom):
        self.screen = screen
        self.zoom = zoom


    def draw_cells(self, positions, color):
        """Draws the live cells on the screen."""
        for col, row in positions:
            pygame.draw.rect(
                self.screen,
                color,
                (col * self.zoom,
                 row * self.zoom,
                 self.zoom,
                 self.zoom)
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