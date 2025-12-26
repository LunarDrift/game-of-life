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
            WIDTH // self.settings.tile_size,
            HEIGHT // self.settings.tile_size
        )
        self.view = LifeView(self.screen, self.settings.tile_size)
        self.controls = ControlsMenu()

        # Keep track of previous settings to detect changes
        self.prev_tile_size = self.settings.tile_size
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
                WIDTH // self.settings.tile_size,
                HEIGHT // self.settings.tile_size
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
        if self.settings.open:
            return
        
        mouse_pressed = pygame.mouse.get_pressed()
        # Click and drag to draw new cells
        x, y = pygame.mouse.get_pos()
        col = x // self.settings.tile_size
        row = y // self.settings.tile_size
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


    # -------------------- Simulation Update --------------------
    def update_simulation(self):
        self.simulation.update_grid_size(
            WIDTH,
            HEIGHT,
            self.settings.tile_size
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
        if self.prev_tile_size != self.settings.tile_size:
            self.view.tile_size = self.settings.tile_size
            self.simulation.update_grid_size(WIDTH, HEIGHT, self.settings.tile_size)
            self.prev_tile_size = self.settings.tile_size

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

        grid_width = WIDTH // self.settings.tile_size
        grid_height = HEIGHT // self.settings.tile_size
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