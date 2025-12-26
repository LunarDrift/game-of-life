import pygame

class SettingsMenu:
    def __init__(self):
        self.open = False
        self.clicked = False

        # Settings values
        self.update_freq = 30
        self.show_grid = False


        # Layout
        self.button_rect = pygame.Rect(10, 10, 80, 20)
        self.panel_rect = pygame.Rect(10, 35, 180, 200)

        self.speed_slow = pygame.Rect(14, 40, 173, 20)
        self.speed_normal = pygame.Rect(14, 60, 173, 20)
        self.speed_fast = pygame.Rect(14, 80, 173, 20)
        self.speed_very_fast = pygame.Rect(14, 100, 173, 20)

        self.font = pygame.font.SysFont(None, 24)


    def handle_event(self, event):
        # Check if the settings button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.open = not self.open
                self.clicked = True

        if self.open and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.speed_slow.collidepoint(event.pos):
                self.update_freq = 60
            elif self.speed_normal.collidepoint(event.pos):
                self.update_freq = 30
            elif self.speed_fast.collidepoint(event.pos):
                self.update_freq = 10
            elif self.speed_very_fast.collidepoint(event.pos):
                self.update_freq = 1
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False


    def draw(self, screen):
        # Draw semi-transparent Settings button
        button_surf = pygame.Surface(
            (self.button_rect.width, self.button_rect.height),
            pygame.SRCALPHA
        )
        button_surf.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(button_surf, self.button_rect.topleft)

        txt = self.font.render("Settings", True, (255, 255, 0))
        screen.blit(
            txt,
            txt.get_rect(center=self.button_rect.center)
        )

        # if the menu is closed, no need to draw the panel
        if not self.open:
            return
        
        # Draw semi-transparent settings panel
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

        # # Draw settings button
        # pygame.draw.rect(
        #     screen,
        #     (0, 0, 0),
        #     self.button_rect,
        #     border_radius=6
        # )

        # txt = self.font.render("Settings", True, (255, 255, 0))
        # screen.blit(
        #     txt,
        #     txt.get_rect(center=self.button_rect.center)
        # )

        # if not self.open:
        #     return
        
        # # Draw settings panel
        # pygame.draw.rect(
        #     screen,
        #     (40, 40, 40), 
        #     self.panel_rect,
        #     border_radius=8
        # )
        # pygame.draw.rect(
        #     screen,
        #     (200, 200, 0),
        #     self.panel_rect,
        #     2,
        #     border_radius=8
        # )

        # Draw speed buttons
        self._draw_button(screen, self.speed_slow, "Speed: Slow")
        self._draw_button(screen, self.speed_normal, "Speed: Normal")
        self._draw_button(screen, self.speed_fast, "Speed: Fast")
        self._draw_button(screen, self.speed_very_fast, "Speed: Very Fast")


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

        # pygame.draw.rect(
        #     screen,
        #     (120, 120, 120),
        #     rect,
        #     border_radius=4
        # )
        # txt = self.font.render(label, True, (0, 0, 0))
        # screen.blit(txt,
        #             txt.get_rect(center=rect.center)
        #         )