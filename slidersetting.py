import pygame
from constants import WHITE

class SliderSetting:
    def __init__(self, label, slider, panel_rect=None, invert=False):
        self.label = label
        self.slider = slider
        self.panel_rect = panel_rect
        self.invert = invert

        self.font = pygame.font.SysFont("ubuntumono", 13)

    
    def handle_event(self, event):
        # Pass events to the slider
        self.slider.handle_event(event)


    def get_value(self):
        # Return slider value, applying inversion if needed
        val = self.slider.val
        if self.invert:
            val = self.slider.max_val - (val - self.slider.min_val)
        return val
    

    def draw(self, screen):
        # Compute the current value for the label
        current_val = round(self.get_value())

        # Combine label with current value
        display_label = f"{self.label}: {current_val}"

        # Render the label above the slider
        label_surface = self.font.render(display_label, True, WHITE)
        label_rect = label_surface.get_rect(
            centerx=self.slider.rect.centerx
        )
        label_rect.bottom = self.slider.rect.top - 5  # 5 pixels above the slider
        screen.blit(label_surface, label_rect)

        # Draw the slider itself
        self.slider.draw(screen)