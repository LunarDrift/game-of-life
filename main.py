import random
import pygame
from simulation import LifeSimulation
from view import LifeView
from settingsmenu import SettingsMenu
from controlsmenu import ControlsMenu
from constants import WIDTH, HEIGHT, FPS, BLACK, GRAY
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

        # Keep track of previous settings to detect changes
        self.prev_zoom = self.settings.zoom
        self.prev_show_grid = self.settings.show_grid
        self.prev_sim_speed = self.settings.sim_speed
        self.prev_cell_color = self.settings.cell_color

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
                "step": 2,
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
        """Handle scroll wheel events for changing settings values while the menu is open."""
        if event.type != pygame.MOUSEWHEEL:
            return
        
        mouse_pos = pygame.mouse.get_pos()

        # Menu open -> check if over sliders
        if self.settings.open:
            for target in self.scroll_targets:
                if target["rect"].collidepoint(mouse_pos):
                    self._apply_scroll(target, event)
                    return
            
            # Not over any slider -> zoom if over grid
            if not self.settings.panel_rect.collidepoint(mouse_pos):
                self._adjust_zoom(event)
            return
        
        # Menu closed -> always zoom
        self._adjust_zoom(event)


    def _apply_scroll(self, target, event):
        # Determine scroll direction
        direction = 1 if event.y > 0 else -1
        # Calculate the change in value based on scroll step
        delta = direction * target["step"]

        slider = target["sync_slider"]

        # Compute new slider value
        if target.get("invert", False):
            # For inverted slider, scrolling up decreases value
            new_slider_val = slider.val - delta
        else:
            # Normal slider behavior
            new_slider_val = slider.val + delta

        # Constrain within min/max
        new_slider_val = max(
            slider.min_val, min(slider.max_val, new_slider_val)
        )
        slider.set_val(new_slider_val)

        # Update the setting value based on slider
        if target.get("invert", False):
            # Inverted
            value = slider.max_val - (new_slider_val - target["min"])
        else:
            value = new_slider_val


        setattr(self.settings, target["attr"], value)


    def _adjust_zoom(self, event):
        """Adjust zoom level based on scroll wheel input."""
        if event.y > 0:
            self.settings.zoom = min(
                self.settings.zoom + 1,
                self.settings.max_zoom
            )
        elif event.y < 0:
            self.settings.zoom = max(
                self.settings.zoom - 1,
                self.settings.min_zoom
            )

        self.settings.zoom_slider.set_val(self.settings.zoom)


    def _adjust_speed(self, event):
        """Adjust simulation speed based on scroll wheel input."""
        delta = 1 if event.y > 0 else -1

        new_speed = self.settings.speed_slider.val + delta
        new_speed = max(
            self.settings.speed_slider.min_val,
            min(self.settings.speed_slider.max_val, new_speed)
        )

        self.settings.speed_slider.set_val(new_speed)

    
    def _adjust_population(self, event):
        delta = 1 if event.y > 0 else -1

        new_pop = self.settings.initial_population_slider.val + delta
        new_pop = max(0, min(100, new_pop))

        self.settings.initial_population_slider.set_val(new_pop)


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

        # Step the simulation while playing
        if self.playing:
            self.count += 1

            # For inverted sliders, calc actual simulation ticks
            actual_speed = self.settings.sim_speed
            # Ex. if speed slider is inverted
            # max_val = slider max, min_val = slider min
            max_val = self.settings.speed_slider.max_val
            min_val = self.settings.speed_slider.min_val
            actual_speed = self.settings.get_speed()

            if self.count >= actual_speed:
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

        if self.prev_cell_color != self.settings.cell_color:
            # If something depends on cell_color, update it here
            self.prev_cell_color = self.settings.cell_color

############################## END UPDATE ##############################

############################## DRAWING ##############################
# Draw all updated game elements to the screen

    def draw(self):
        self.screen.fill(GRAY)
        self.view.draw_cells(self.simulation.positions, self.settings.cell_color)

        grid_width = WIDTH // self.settings.zoom
        grid_height = HEIGHT // self.settings.zoom
        self.view.draw_grid(
            grid_width,
            grid_height,
            BLACK,
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