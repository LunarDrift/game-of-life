import random
import pygame
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
from simulation import LifeSimulation
from view import LifeView
from settingsmenu import SettingsMenu


pygame.init()


BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (200, 200, 0)

WIDTH, HEIGHT= 800, 800
TILE_SIZE = 10
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 120

MIN_POSITIONS = 5
MAX_POSITIONS = 20



class LifeGame:
    def __init__(self):
        

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()

        self.simulation = LifeSimulation(GRID_WIDTH, GRID_HEIGHT)
        self.view = LifeView(self.screen, TILE_SIZE)
        self.settings = SettingsMenu()

    def main(self):
        self.running = True
        self.playing = False
        self.count = 0
        self.update_freq = 30
        self.show_grid = False


        # -------------- UI WIDGETS --------------
        speed_dropdown = Dropdown(
            self.screen,
            10, 10, 140, 40,
            name='Update Speed',
            choices=[
                'Slow (60)',
                'Normal (30)',
                'Fast (10)',
                'Very Fast (1)'
            ],
            values=[60, 30, 10, 1],
            direction='down',
            textHAlign='left'
        )


        while self.running:
            self.clock.tick(FPS)

            # ---------------------------------------------------- EVENTS ----------------------------------------------------

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # -------------------------------------------- Mouse Events --------------------------------------------
                if pygame.mouse.get_pressed()[0]:
                    # Click and drag to draw new cells
                    x, y = pygame.mouse.get_pos()
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)

                    if 0 <= col <= GRID_WIDTH and 0 <= row <= GRID_HEIGHT:
                        self.simulation.positions.add(pos)

                if pygame.mouse.get_pressed()[2]:
                    # Right click to remove a cell
                    x, y = pygame.mouse.get_pos()
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)

                    if pos in self.simulation.positions:
                        # Remove position if it already exists
                        self.simulation.positions.remove(pos)
            # -------------------------------------------- Keyboard Events --------------------------------------------
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
                        self.simulation.positions = self.simulation.gen(random.randrange(MIN_POSITIONS, MAX_POSITIONS) * GRID_WIDTH)
                    elif event.key == pygame.K_g:
                        # Toggle grid lines
                        self.show_grid = not self.show_grid
                    
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                
                


            # ---------------------------------------------------- UPDATE ----------------------------------------------------
            if self.playing:
                self.count += 1
                if self.count >= self.update_freq:
                    self.count = 0
                    self.simulation.step()


            pygame.display.set_caption("Playing" if self.playing else "Paused")

            selected_speed = speed_dropdown.getSelected()
            if selected_speed is not None:
                self.update_freq = selected_speed


            # ---------------------------------------------------- DRAW ------------------------------------------------------

            self.screen.fill(GRAY)
            self.view.draw_cells(self.simulation.positions, YELLOW)
            self.view.draw_grid(GRID_WIDTH, GRID_HEIGHT, BLACK, self.show_grid)

            pygame_widgets.update(events)
            pygame.display.flip()


        pygame.quit()


if __name__ == "__main__":
    game = LifeGame()
    game.main()