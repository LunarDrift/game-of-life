import pygame


class ToggleButton:
    def __init__(
        self,
        rect,
        label,
        value=False,
        on_color=(80, 160, 80),
        off_color=(120, 120, 120),
        text_color=(255, 255, 255),
        font=None,
    ):
        self.rect = rect
        self.label = label
        self.value = value
        self.on_color = on_color
        self.off_color = off_color
        self.text_color = text_color
        self.font = font or pygame.font.SysFont("ubuntumono", 13)

    
    def set_value(self, value: bool):
        self.value = value


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.value = not self.value
                return True
        return False

    
    def draw(self, screen):
        color = self.on_color if self.value else self.off_color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)

        label = f"{self.label}: {'ON' if self.value else 'OFF'}"
        txt = self.font.render(label, True, self.text_color)
        screen.blit(txt, txt.get_rect(center=self.rect.center))
