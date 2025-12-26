import pygame

class SimpleSlider:
    def __init__(self, x, y, w, h, min_val, max_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = max_val // 2  # Start in the middle
        self.grabbed = False
        # The "handle" of the slider
        self.handle_rect = pygame.Rect(
            x + (w // 2) - (x // 2),    # Center handle initially
            y,
            10,
            h
        )

    def set_val(self, val):
        self.val = max(self.min_val, min(val, self.max_val))

        # Convert value - percentage
        percent = (self.val - self.min_val) / (self.max_val - self.min_val)
        # Update handle position
        self.handle_rect.centerx = (
            self.rect.left + percent * self.rect.width
        )

    
    def _update_value_from_mouse(self, mouse_x):
        # Calculate relative position of mouse to slider
        rel_x = mouse_x - self.rect.x
        # Constrain within slider width
        rel_x = max(0, min(rel_x, self.rect.width))

        # Calculate value based on position
        ratio = rel_x / self.rect.width
        self.val = self.min_val + ratio * (self.max_val - self.min_val)

        # Update handle position
        self.handle_rect.centerx = self.rect.x + rel_x


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.grabbed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed = False

        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                # Move handle and constrain to the bar
                self.handle_rect.centerx = max(self.rect.left, min(event.pos[0], self.rect.right))
                # Calculate value
                pos = (self.handle_rect.centerx - self.rect.left) / self.rect.width
                self.val = self.min_val + (pos * (self.max_val - self.min_val))


    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            self.rect
        )
        # Draw the handle
        pygame.draw.rect(
            screen,
            (200, 200, 200),
            self.handle_rect
        )

# Usage in your loop:
# slider = SimpleSlider(50, 50, 200, 20, 0, 100)
# slider.handle_event(event)
# slider.draw(screen)