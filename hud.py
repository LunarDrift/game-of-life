import pygame
from constants import BUTTON_LABEL_COLOR

class HUD:
    def __init__(self, font):
        # -------------------------------------------------
        # HUD attributes
        # -------------------------------------------------
        self.font = font
        self.generations = 0
        self.cell_count = 0
        self.clock = None


    def _draw_hud_bar(self, screen):
        """Draw a semi-transparent HUD bar at the top of the screen."""
        hud_height = 23
        hud_bar = pygame.Surface((screen.get_width(), hud_height), pygame.SRCALPHA)
        hud_bar.fill((0, 0, 0, 150))  # Semi-transparent black
        screen.blit(hud_bar, (0, 0))

    def _draw_element_bg(self, screen, text, position):
        """Draw background for HUD elements."""
        bg = pygame.Surface(
            (text.get_width() + 10, text.get_height() + 6),
            pygame.SRCALPHA
        )
        bg.fill((0, 0, 0, 120))  # Semi-transparent background
        screen.blit(bg, position)
    
    def _draw_generation_tracker(self, screen, generations):
        """Display the current generation count on the screen."""
        position = (screen.get_width() // 2 - 60, 0)
        text = self.font.render(f"Generation: {generations}", True, BUTTON_LABEL_COLOR)
        self._draw_element_bg(screen, text, position)
        screen.blit(text, (position[0] + 5, position[1] + 3))

    def _draw_fps_tracker(self, screen, clock):
        """Display the current FPS on the screen."""
        position = (screen.get_width() - 60, 0)
        text = self.font.render(f"FPS:{int(clock.get_fps())}", True, BUTTON_LABEL_COLOR)
        self._draw_element_bg(screen, text, position)
        screen.blit(text, (position[0] + 5, position[1] + 3))

    def draw_cell_count(self, screen, cell_count):
        """Display the current live cell count on the screen."""
        position = (screen.get_width() - 150, 0)
        text = self.font.render(f"Cells: {cell_count}", True, BUTTON_LABEL_COLOR)
        self._draw_element_bg(screen, text, position)
        screen.blit(text, (position[0] + 5, position[1] + 3))

    def update(self, generations=None, cell_count=None, clock=None):
        """Update HUD data."""
        if generations is not None:
            self.generations = generations
        if cell_count is not None:
            self.cell_count = cell_count
        if clock is not None:
            self.clock = clock
    
    def draw(self, screen):
        """Draw all HUD elements."""
        self._draw_hud_bar(screen)
        self._draw_generation_tracker(screen, self.generations)
        self._draw_fps_tracker(screen, self.clock)
        self.draw_cell_count(screen, self.cell_count)