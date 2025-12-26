import pygame

class SimpleSlider:
    def __init__(self, x, y, w, h, min_val, max_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = min_val
        self.grabbed = False
        # The "handle" of the slider
        self.handle_rect = pygame.Rect(x, y, 10, h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            # Move handle and constrain to the bar
            self.handle_rect.centerx = max(self.rect.left, min(event.pos[0], self.rect.right))
            # Calculate value
            pos = (self.handle_rect.centerx - self.rect.left) / self.rect.width
            self.val = self.min_val + (pos * (self.max_val - self.min_val))

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect) # The bar
        pygame.draw.rect(screen, (200, 200, 200), self.handle_rect) # The handle

# Usage in your loop:
# slider = SimpleSlider(50, 50, 200, 20, 0, 100)
# slider.handle_event(event)
# slider.draw(screen)