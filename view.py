import pygame


class LifeView:
    def __init__(self, screen, tile_size):
        self.screen = screen
        self.tile_size = tile_size


    def draw_cells(self, positions, color):
        """Draws the live cells on the screen."""
        for col, row in positions:
            pygame.draw.rect(
                self.screen,
                color,
                (col * self.tile_size,
                 row * self.tile_size,
                 self.tile_size,
                 self.tile_size)
            )


    def draw_grid(self, width, height, color, show=False):
        """Draws the grid lines on the screen."""
        if show:
            for x in range(width):
                pygame.draw.line(
                    self.screen,
                    color,
                    (x * self.tile_size, 0),
                    (x * self.tile_size, height * self.tile_size)
                )
            for y in range(height):
                pygame.draw.line(
                    self.screen,
                    color,
                    (0, y * self.tile_size),
                    (width * self.tile_size, y * self.tile_size)
                )