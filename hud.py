import pygame
from constants import BUTTON_LABEL_COLOR

class HUD:
    def __init__(self, font):
        # -------------------------------------------------
        # HUD attributes
        # -------------------------------------------------
        self.font = font


    def draw_hud_bar(self, screen):
        """Draw a semi-transparent HUD bar at the top of the screen."""
        hud_height = 25
        hud_bar = pygame.Surface((screen.get_width(), hud_height), pygame.SRCALPHA)
        hud_bar.fill((0, 0, 0, 120))  # Semi-transparent black
        screen.blit(hud_bar, (0, 0))

    
    def draw_generation_tracker(self, screen, generations):
        """Display the current generation count on the screen.

        :generations: current generation count
        :font: pygame Font object for rendering text
        :color: RGB tuple for text color
        :position: (x, y) tuple for text position
        """
        position = (screen.get_width() - 105, 0)
        text = self.font.render(f"Generation: {generations}", True, BUTTON_LABEL_COLOR)
        # bg = pygame.Surface(
        #     (text.get_width() + 10, text.get_height() + 6),
        #     pygame.SRCALPHA
        # )
        # bg.fill((0, 0, 0, 120))  # Semi-transparent background
        # screen.blit(bg, position)
        screen.blit(text, (position[0] + 5, position[1] + 3))

    
    def draw(self, screen, generations):
        """Draw all HUD elements."""
        self.draw_hud_bar(screen)
        self.draw_generation_tracker(screen, generations)