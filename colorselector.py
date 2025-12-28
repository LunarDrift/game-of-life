import pygame
from constants import WHITE, YELLOW

class ColorSelector:
    def __init__(self, color_buttons, font):
        self.color_buttons = color_buttons
        self.selected_color = YELLOW
        self.font = font

    
    def _draw_button(self, screen, rect, color):
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)  # White border


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, color in self.color_buttons:
                if rect.collidepoint(event.pos):
                    self.selected_color = color


    def draw(self, screen, panel_rect):
        # Draw all color color_buttons
        color_label_surface = self.font.render(
            "Cell Colors", True, WHITE
        )
        color_label_rect = color_label_surface.get_rect(
            centerx=panel_rect.centerx
        )
        color_label_rect.bottom = 160
        screen.blit(color_label_surface, color_label_rect)

        # Draw label "Cell Colors"
        for rect, color in self.color_buttons:
            self._draw_button(screen, rect, color)
        
