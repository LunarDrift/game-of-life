import pygame


class ControlsMenu:
    def __init__(self):
        self.open = False
        self.clicked = False

        # Controls button and panel rectangles
        self.button_rect = pygame.Rect(90, 5, 80, 20)
        self.panel_rect = pygame.Rect(90, 26, 260, 175)

        # Font for button labels
        self.font = pygame.font.SysFont("ubuntumono", 13)


    def _draw_button(self, screen, rect, label):

        # Draw semi-transparent button
        button_surf = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )
        button_surf.fill((120, 120, 120, 100))  # Semi-transparent gray
        screen.blit(button_surf, rect.topleft)

        txt = self.font.render(label, True, (0, 0, 0))
        screen.blit(
            txt,
            txt.get_rect(center=rect.center)
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
        button_surf = pygame.Surface(
            (self.button_rect.width, self.button_rect.height),
            pygame.SRCALPHA
        )
        button_surf.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(button_surf, self.button_rect.topleft)

        button_txt = self.font.render("Controls", True, (235, 235, 0))
        screen.blit(
            button_txt,
            button_txt.get_rect(center=self.button_rect.center)
        )

        # if the menu is closed, no need to draw the panel
        if not self.open:
            return
        
        # Draw semi-transparent controls panel
        panel_surf = pygame.Surface(
            (self.panel_rect.width, self.panel_rect.height),
            pygame.SRCALPHA
        )
        panel_surf.fill((40, 40, 40, 150)) # Semi-transparent dark gray
        screen.blit(panel_surf, self.panel_rect.topleft)

        # Draw panel border
        pygame.draw.rect(
            screen,
            (200, 200, 0),
            self.panel_rect,
            2,
            border_radius=8
        )

        # Draw control instructions
        instructions = [
            "Controls:",
            "• Left Click:  Create New Cell",
            "• Right Click: Delete Cell",
            "• Mouse Wheel: Zoom In/Out",
            "• Spacebar: Start/Pause Simulation",
            "• R: Generate Random Seed",
            "• C: Clear All Cells",
            "• G: Toggle Grid On/Off",
        ]

        for i, line in enumerate(instructions):
            instr_surf = self.font.render(line, True, (255, 255, 255))
            screen.blit(
                instr_surf,
                (self.panel_rect.x + 10, self.panel_rect.y + 10 + i * 20)
            )