import random
import pygame
from simulation import LifeSimulation
from view import LifeView
from settingsmenu import SettingsMenu
from constants import WIDTH, HEIGHT, FPS, BLACK, GRAY, YELLOW

pygame.init()

class LifeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()

        self.settings = SettingsMenu()
        self.simulation = LifeSimulation(
            WIDTH // self.settings.tile_size,
            HEIGHT // self.settings.tile_size
        )
        self.view = LifeView(self.screen, self.settings.tile_size)

    def main(self):
        running = True
        self.playing = False
        self.count = 0

        while running:
            self.clock.tick(FPS)

# ---------------------------------------------------- EVENTS ----------------------------------------------------

            events = pygame.event.get()
            for event in events:
                # Let settings menu handle its own clicks
                self.settings.handle_event(event)
                if event.type == pygame.QUIT:
                    running = False

            # -------------------------------- Keyboard Input --------------------------------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Pause or unpause the game
                        self.playing = not self.playing
                    elif event.key == pygame.K_c:
                        # Clear the grid
                        self.simulation.positions.clear()
                        self.playing = False
                        self.count = 0
                    elif event.key == pygame.K_r:
                        # Generate random positions for cells
                        num_cells = random.randrange(
                            self.settings.min_cells,
                            self.settings.max_cells
                        ) * self.simulation.width
                        self.simulation.positions = self.simulation.gen(num_cells)
                    elif event.key == pygame.K_g:
                        # Toggle grid lines
                        self.settings.show_grid = not self.settings.show_grid
                    
                    elif event.key == pygame.K_ESCAPE:
                        running = False

# ---------------------------------------------------- UPDATE ----------------------------------------------------
            
            # Compute grid size from current tile size
            grid_width = WIDTH // self.settings.tile_size
            grid_height = HEIGHT // self.settings.tile_size

            # Update simulation grid size based on current tile size
            self.simulation.update_grid_size(WIDTH, HEIGHT, self.settings.tile_size)
            # Keep track of previous tile size and update view if it has changed
            if self.view.tile_size != self.settings.tile_size:
                self.view.tile_size = self.settings.tile_size

            # Mouse Drawing
            if not self.settings.open:
                mouse_pressed = pygame.mouse.get_pressed()
                # Click and drag to draw new cells
                x, y = pygame.mouse.get_pos()
                col = x // self.settings.tile_size
                row = y // self.settings.tile_size
                pos = (col, row)

                if mouse_pressed[0]:
                    # Left click to add a cell
                    if 0 <= col < self.simulation.width \
                    and 0 <= row < self.simulation.height:
                        self.simulation.positions.add(pos)

                elif mouse_pressed[2]:
                    # Right click to remove a cell
                    if pos in self.simulation.positions:
                        # Remove position if it already exists
                        self.simulation.positions.remove(pos)

            # Step the simulation based on update frequency
            if self.playing:
                self.count += 1
                if self.count >= self.settings.update_freq:
                    self.count = 0
                    self.simulation.step()            


# ---------------------------------------------------- DRAW ------------------------------------------------------

            self.screen.fill(GRAY)
            self.view.draw_cells(self.simulation.positions, YELLOW)
            self.view.draw_grid(
                grid_width,
                grid_height,
                BLACK,
                self.settings.show_grid
            )
            self.settings.draw(self.screen)


            pygame.display.set_caption("Playing" if self.playing else "Paused")
            pygame.display.flip()


        pygame.quit()


if __name__ == "__main__":
    game = LifeGame()
    game.main()