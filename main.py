import random
import pygame
from simulation import LifeSimulation
from view import LifeView
from settingsmenu import SettingsMenu
from controlsmenu import ControlsMenu
from constants import WIDTH, HEIGHT, FPS, BLACK, GRAY, YELLOW

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


#################################### HELPER METHODS ####################################

    def reset_cells(self, grid_width, grid_height):
        self.simulation.positions.clear()

        # Probability-based generation for cells
        prob_alive = self.settings.initial_population_slider.val / 100
        positions = set()
        
        for col in range(grid_width):
            for row in range(grid_height):
                if random.random() < prob_alive:
                    positions.add((col, row))
        self.simulation.positions = positions


    # -------------------- Event Handling --------------------
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False

            self.settings.handle_event(event)
            self.handle_scrollwheel(event)
            self.controls.handle_event(event)
            self.handle_keyboard(event)
        
        return True


    def handle_keyboard(self, event):
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
            self.reset_cells(
                WIDTH // self.settings.zoom,
                HEIGHT // self.settings.zoom
            )

        elif event.key == pygame.K_g:
            # Toggle grid lines
            self.settings.show_grid = not self.settings.show_grid
        
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

    # -------------------- Mouse Drawing --------------------
    def handle_mouse(self):
        # Mouse Drawing
        if not self.can_draw():
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

    
    def handle_scrollwheel(self, event):
        """Handle scroll wheel events for changing settings values while the menu is open."""
        if event.type != pygame.MOUSEWHEEL:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        menu_open = self.settings.open
        over_panel = self.settings.panel_rect.collidepoint(mouse_pos)
        over_zoom_slider = (
            self.settings.zoom_slider.rect.collidepoint(mouse_pos)
        )

        should_zoom = False

        if not menu_open:
            should_zoom = True
        else:
            if over_zoom_slider:
                should_zoom = True
            elif not over_panel:
                should_zoom = True
        if not should_zoom:
            return
        
        # Apply zoom changes
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

        # Keep slider in sync
        self.settings.zoom_slider.set_val(self.settings.zoom)


    def can_draw(self):
        if self.settings.open or self.controls.open:
            return False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.settings.button_rect.collidepoint((mouse_x, mouse_y)):
            return False
        elif self.controls.button_rect.collidepoint((mouse_x, mouse_y)):
            return False
        return True


    # -------------------- Simulation Update --------------------
    def update_simulation(self):
        self.simulation.update_grid_size(
            WIDTH,
            HEIGHT,
            self.settings.zoom
        )

        self.update_simulation_settings()

        # Step the simulation based on simulation speed
        if self.playing:
            self.count += 1
            if self.count >= self.settings.sim_speed:
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


    # -------------------- Drawing --------------------
    def draw(self):
        self.screen.fill(GRAY)
        self.view.draw_cells(self.simulation.positions, YELLOW)

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


    # -------------------- Main Loop --------------------
    def main(self):
        running = True
        self.playing = False
        self.count = 0

        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.handle_mouse()
            self.update_simulation()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = LifeGame()
    game.main()