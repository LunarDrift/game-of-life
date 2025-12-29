import pygame
from constants import (
    WHITE, PANEL_COLOR, PANEL_BORDER_COLOR, BUTTON_LABEL_COLOR, BUTTON_COLOR
)


class ControlsMenu:
    """Menu displaying control instructions with toggle button."""
    def __init__(self):
        self.open = False
        self.clicked = False

        # Controls button and panel rectangles
        self.button_rect = pygame.Rect(90, 5, 80, 20)
        self.panel_rect = pygame.Rect(90, 26, 260, 195)

        # Font for button labels
        self.font = pygame.font.SysFont("ubuntumono", 13)


    def _draw_button(self, screen, rect, label=None, label_color=(0, 0, 0), color=(120, 120, 120, 100)):
        """Draw a semi-transparent button with optional label."""
        button_surf = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )
        button_surf.fill(color)  # Semi-transparent gray by default
        screen.blit(button_surf, rect.topleft)

        txt = self.font.render(label, True, label_color)
        screen.blit(
            txt,
            txt.get_rect(center=rect.center)
        )

    
    def _draw_panel(self, screen):
        """Draw the main controls panel background and border."""
        panel_surf = pygame.Surface(
            (self.panel_rect.width, self.panel_rect.height),
            pygame.SRCALPHA
        )
        panel_surf.fill(PANEL_COLOR) # Semi-transparent dark gray
        screen.blit(panel_surf, self.panel_rect.topleft)

        # Draw panel border
        pygame.draw.rect(
            screen,
            PANEL_BORDER_COLOR,
            self.panel_rect,
            2,
            border_radius=8
        )

    def _draw_instructions(self, screen):
        """Draw control instructions inside the panel."""
        instructions = [
            "Controls:",
            "• Left Click:  Create New Cell",
            "• Right Click: Delete Cell",
            "• Mouse Wheel: Zoom In/Out",
            "• Spacebar: Start/Pause Simulation",
            "• R: Generate Random Seed",
            "• C: Clear All Cells",
            "• G: Toggle Grid On/Off",
            "• F: Toggle Cell Fading On/Off",
        ]

        for i, line in enumerate(instructions):
            instr_surf = self.font.render(line, True, WHITE)
            screen.blit(
                instr_surf,
                (self.panel_rect.x + 10, self.panel_rect.y + 10 + i * 20)
            )

    
    def handle_event(self, event):
        # Toggle menu open/close on button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.open = not self.open
                self.clicked = True

        # Close menu if clicking outside panel when open
        if self.open and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (
                not self.panel_rect.collidepoint(event.pos)
                and not self.button_rect.collidepoint(event.pos)
            ):
                self.open = False
        
        # Release clicked state
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

    
    def draw(self, screen):
        # Draw semi-transparent Controls button
        self._draw_button(
            screen,
            self.button_rect,
            label="Controls",
            label_color=BUTTON_LABEL_COLOR,
            color=BUTTON_COLOR
        )

        # if the menu is closed, no need to draw the panel
        if not self.open:
            return
        # Draw semi-transparent controls panel
        self._draw_panel(screen)
        # Draw control instructions
        self._draw_instructions(screen)