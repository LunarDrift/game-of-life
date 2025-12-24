import random
import pygame
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


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()


def gen(num):
    """Generate `num` amount of random positions on the grid."""
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])



def draw_grid(show=False):
    """Draws the grid lines on the screen."""
    if show:
        for row in range(GRID_HEIGHT):
            pygame.draw.line(
                screen,
                BLACK,
                (0, row * TILE_SIZE),
                (WIDTH, row * TILE_SIZE)
            )
        for col in range(GRID_WIDTH):
            pygame.draw.line(
                screen,
                BLACK,
                (col * TILE_SIZE, 0),
                (col * TILE_SIZE, HEIGHT)
            )


def fill_grid(positions):
    """Fills the grid with live cells at the given positions."""
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(
            screen,
            YELLOW,
            (*top_left, TILE_SIZE, TILE_SIZE)
        )


def adjust_grid(positions):
    """Adjusts the grid based on the rules of Conway's Game of Life."""
    all_neighbors = set()  # To store all neighbors of live cells
    new_positions = set()  # To store the new positions of live cells

    # Loop through all live cells
    for pos in positions:
        # Get neighbors of this position
        neighbors = get_neighbors(pos)
        # Add these neighbors to the all_neighbors set
        all_neighbors.update(neighbors)

        # Check if neighbors are alive
        # loop through neighbors; passed in as x; is x in positions? if so, keep it; if not, remove it
        # filter() gives us an iterator; need to convert it back to a list
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            # Does this position have 2 or 3 neighbors? If so, it stays alive.
            new_positions.add(pos)

    # Loop through all neighbors of live cells
    for pos in all_neighbors:
        # Get neighbors of this position
        neighbors = get_neighbors(pos)
        neighbors = list(filter(lambda x: x in positions, neighbors))
        # If a dead cell has exactly 3 live neighbors, it becomes alive.
        if len(neighbors) == 3:
            new_positions.add(pos)
    
    return new_positions


def get_neighbors(position):
    """Returns an array or set that contains all neighboring positions of a given position."""
    x, y = position
    neighbors = []
    for dx in [-1, 0, 1]:
        # Skip out-of-bounds neighbors
        if x + dx < 0 or x + dx >= GRID_WIDTH:
            continue

        for dy in [-1, 0, 1]:
            # Skip out-of-bounds neighbors
            if y + dy < 0 or y + dy >= GRID_HEIGHT:
                continue

            if dx == 0 and dy == 0:
                # This is the cell itself, not a neighbor; ignore
                continue  

            neighbors.append((x + dx, y + dy))

    return neighbors


def main():
    running = True
    playing = False
    count = 0
    update_freq = 30
    show_grid = False

    positions = set()
    while running:
        clock.tick(FPS)

        # ---------------------------------------------------- EVENTS ----------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------------------------------------------- Mouse Events --------------------------------------------
            if pygame.mouse.get_pressed()[0]:
                # Click and drag to draw new cells
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if 0 <= col <= GRID_WIDTH and 0 <= row <= GRID_HEIGHT:
                    positions.add(pos)


            if pygame.mouse.get_pressed()[2]:
                # Right click to remove a cell
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    # Remove position if it already exists
                    positions.remove(pos)
        # -------------------------------------------- Keyboard Events --------------------------------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Pause or unpause the game
                    playing = not playing
                elif event.key == pygame.K_c:
                    # Clear the grid
                    positions.clear()
                    playing = False
                    count = 0
                elif event.key == pygame.K_r:
                    # Generate random positions for cells
                    positions = gen(random.randrange(MIN_POSITIONS, MAX_POSITIONS) * GRID_WIDTH)
                
                elif event.key == pygame.K_g:
                    # Toggle grid lines
                    show_grid = not show_grid
                
                
                elif event.key == pygame.K_ESCAPE:
                    running = False


        # ---------------------------------------------------- UPDATE ----------------------------------------------------
        if playing:
            count += 1
            if count >= update_freq:
                count = 0
                positions = adjust_grid(positions)


        pygame.display.set_caption("Playing" if playing else "Paused")


        # ---------------------------------------------------- DRAW ------------------------------------------------------

        screen.fill(GRAY)
        fill_grid(positions)
        draw_grid(show_grid)
        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":
    main()