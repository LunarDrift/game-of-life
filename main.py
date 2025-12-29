import random
import pygame
from simulation import LifeSimulation
from view import LifeView
from settingsmenu import SettingsMenu
from controlsmenu import ControlsMenu
from colorselector import ColorSelector
from constants import WIDTH, HEIGHT, FPS, GRAY, GRID_COLOR
from debug import debug

pygame.init()

class LifeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        self.running = True

        self.settings = SettingsMenu()
        self.simulation = LifeSimulation(
            WIDTH // self.settings.zoom,
            HEIGHT // self.settings.zoom
        )
        self.view = LifeView(self.screen, self.settings.zoom)
        self.controls = ControlsMenu()
        self.color_selector = ColorSelector(
            self.settings.color_buttons,
            self.settings.font
        )

        # Keep track of previous settings to detect changes
        self.prev_zoom = self.settings.zoom
        self.prev_show_grid = self.settings.show_grid
        self.prev_sim_speed = self.settings.sim_speed
        self.prev_cell_color = self.color_selector.selected_color
        self.prev_fade_enabled = self.settings.fade_enabled

        # Scroll wheel targets for adjusting settings
        self.scroll_targets = [
            {
                "rect": self.settings.zoom_slider.rect,
                "attr": "zoom",
                "min": self.settings.min_zoom,
                "max": self.settings.max_zoom,
                "step": 1,
                "sync_slider": self.settings.zoom_slider,
                "invert": False,
            },
            {
                "rect": self.settings.speed_slider.rect,
                "attr": "sim_speed",
                "min": self.settings.min_update_freq,
                "max": self.settings.max_update_freq,
                "step": 5,
                "sync_slider": self.settings.speed_slider,
                "invert": True,
            },
            {
                "rect": self.settings.initial_population_slider.rect,
                "attr": "initial_cells",
                "min": 0,
                "max": 100,
                "step": 5,
                "sync_slider": self.settings.initial_population_slider,
                "invert": False,
            },
        ]


############################## HELPER METHODS ##############################
# Internal methods for handling input and game logic

    def _handle_keyboard(self, event):
        if event.type != pygame.KEYDOWN:
            return
        
        if event.key == pygame.K_SPACE:
            # Pause or unpause the game
            self.playing = not self.playing

        elif event.key == pygame.K_c:
            # Clear the grid and pause the simulation
            self.simulation.positions.clear()
            self.playing = False
            self.count = 0

        elif event.key == pygame.K_r:
            self._reset_cells(
                WIDTH // self.settings.zoom,
                HEIGHT // self.settings.zoom
            )

        elif event.key == pygame.K_g:
            # Toggle grid lines
            self.settings.show_grid = not self.settings.show_grid
        
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()


    def _handle_mouse(self):
        # Mouse Drawing
        if not self._can_draw():
            return
        
        mouse_pressed = pygame.mouse.get_pressed()
        # Click and drag to draw new cells
        x, y = pygame.mouse.get_pos()
        col = x // self.settings.zoom
        row = y // self.settings.zoom
        pos = (col, row)

        if mouse_pressed[0]:
            # Left click to add a cell
            if 0 <= col < self.simulation.width and \
            0 <= row < self.simulation.height:
                self.simulation.positions.add(pos)

        elif mouse_pressed[2]:
            # Right click to remove a cell
            if pos in self.simulation.positions:
                # Remove position if it already exists
                self.simulation.positions.remove(pos)


    def _handle_scrollwheel(self, event):
        """Handle mouse wheel events for sliders and zoom."""
        if event.type != pygame.MOUSEWHEEL:
            return

        mouse_pos = pygame.mouse.get_pos()
        settings = self.settings
        target_slider = None

        if settings.open:
            for slider_setting in settings.sliders:
                if slider_setting.slider.rect.collidepoint(mouse_pos):
                    target_slider = slider_setting
                    break

            # Still want zoom functionality when menu is open, if mouse not in panel  
            if not target_slider and not settings.panel_rect.collidepoint(mouse_pos):
                target_slider = next(
                    s for s in settings.sliders if "zoom" in s.label.lower()
                )

        else:
            target_slider = next(
                s for s in settings.sliders if "zoom" in s.label.lower()
            )

        # Apply scroll to the target slider
        if target_slider:
            step = target_slider.step
            delta = step if event.y > 0 else -step
            slider = target_slider.slider
            new_val = slider.val + delta

            # Clamp value within slider min/max
            new_val = max(slider.min_val, min(slider.max_val, new_val))
            slider.set_val(new_val)

            # Update corresponding setting in settings
            if getattr(target_slider, "invert", False):
                value = slider.max_val - (new_val - slider.min_val)
            else:
                value = new_val

            # Map slider base_label to actual settings attribute
            label_lower = target_slider.label.lower()
            if "zoom" in label_lower:
                settings.zoom = value
            elif "speed" in label_lower:
                settings.sim_speed = value
            elif "population" in label_lower:
                settings.initial_cells = value


    def _reset_cells(self, grid_width, grid_height):
        self.simulation.positions.clear()

        # Probability-based generation for cells
        prob_alive = self.settings.initial_population_slider.val / 100
        positions = set()
        
        for col in range(grid_width):
            for row in range(grid_height):
                if random.random() < prob_alive:
                    positions.add((col, row))
        self.simulation.positions = positions

    
    def _can_draw(self):
        if self.settings.open or self.controls.open:
            return False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.settings.button_rect.collidepoint((mouse_x, mouse_y)):
            return False
        elif self.controls.button_rect.collidepoint((mouse_x, mouse_y)):
            return False
        return True

############################## END HELPER METHODS ##############################

############################## EVENTS ##############################
# Handle all pygame events (keyboard, mouse, etc.)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False

            self.settings.handle_event(event)
            self._handle_scrollwheel(event)
            self.controls.handle_event(event)
            self._handle_keyboard(event)
            if self.settings.open:
                self.color_selector.handle_event(event)
        
        return True    

############################## END EVENTS ##############################

############################## UPDATE ##############################
# Update simulation state and settings based on events

    def update_simulation(self):
        self.simulation.update_grid_size(
            WIDTH,
            HEIGHT,
            self.settings.zoom
        )

        self.update_simulation_settings()
        self.view.update_fade(self.simulation.positions)

        # Step the simulation while playing
        if self.playing:
            self.count += 1

            if self.count >= self.settings.get_speed():
                self.count = 0
                self.simulation.step()
            

    def update_simulation_settings(self):
        # Update dependent settings in simulation if they have changed
        if self.prev_zoom != self.settings.zoom:
            self.view.zoom = self.settings.zoom
            self.simulation.update_grid_size(WIDTH, HEIGHT, self.settings.zoom)
            self.prev_zoom = self.settings.zoom

        if self.prev_show_grid != self.settings.show_grid:
            # If something depends on show_grid, update it here
            self.prev_show_grid = self.settings.show_grid

        if self.prev_sim_speed != self.settings.sim_speed:
            # If we use sim_speed elsewhere, we can update it here
            self.prev_sim_speed = self.settings.sim_speed

        if self.prev_cell_color != self.color_selector.selected_color:
            # If something depends on cell_color, update it here
            self.prev_cell_color = self.color_selector.selected_color

        if self.prev_fade_enabled != self.settings.fade_enabled:
            self.view.set_fade_enabled(self.settings.fade_enabled)
            self.prev_fade_enabled = self.settings.fade_enabled

############################## END UPDATE ##############################

############################## DRAWING ##############################
# Draw all updated game elements to the screen

    def draw(self):
        self.screen.fill(GRAY)
        self.view.draw_cells(self.simulation.positions, self.color_selector.selected_color)

        grid_width = int(WIDTH // self.settings.zoom)
        grid_height = int(HEIGHT // self.settings.zoom)
        self.view.draw_grid(
            grid_width,
            grid_height,
            GRID_COLOR,
            self.settings.show_grid
        )

        self.settings.draw(self.screen)
        self.controls.draw(self.screen)

        pygame.display.set_caption("Playing" if self.playing else "Paused")
        pygame.display.flip()

############################## END DRAWING ##############################

############################## MAIN LOOP ##############################

    def main(self):
        running = True
        self.playing = False
        self.count = 0

        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self._handle_mouse()
            self.update_simulation()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = LifeGame()
    game.main()
