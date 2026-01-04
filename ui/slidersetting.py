import pygame
from constants import WHITE

class SliderSetting:
    """Slider with label and value display."""
    def __init__(self, label, slider, panel_rect=None, step=1, display_value_fn=None):
        self.label = label
        self.slider = slider
        self.panel_rect = panel_rect
        self.step = step
        self.display_value_fn = display_value_fn or (lambda val: round(val))
        self.font = pygame.font.SysFont("ubuntumono", 13)

    
    def handle_event(self, event):
        # Pass events to the slider
        self.slider.handle_event(event)


    def get_value(self):
        return self.slider.val
    

    def draw(self, screen):
        # Compute the current value for the label
        raw_val = self.get_value()
        display_val = self.display_value_fn(raw_val)

        # Combine label with current value
        display_label = f"{self.label}: {display_val}"

        label_surface = self.font.render(display_label, True, WHITE)
        label_rect = label_surface.get_rect(
            centerx=self.slider.rect.centerx
        )
        label_rect.bottom = self.slider.rect.top - 5
        screen.blit(label_surface, label_rect)
        self.slider.draw(screen)