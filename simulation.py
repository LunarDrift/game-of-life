from collections import defaultdict

class LifeSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.positions = set()
        self.generations = 0


    def clear(self):
        self.positions.clear()


    def step(self):
        """Advance the simulation by one generation."""
        self.positions = self._next_generation()
        self.generations += 1

    
    def _next_generation(self):
        """Adjusts the grid based on the rules of Conway's Game of Life."""
        neighbor_counts = defaultdict(int)

        # Count neighbors of all live cells
        for x, y in self.positions:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue  # Skip; this is the cell itself
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbor_counts[(nx, ny)] += 1

        
        new_positions = set()

        # Apply Life rules based on neighbor counts
        for pos, count in neighbor_counts.items():
            if count == 3 or (count == 2 and pos in self.positions):
                new_positions.add(pos)

        return new_positions
    

    def update_grid_size(self, width, height, tile_size):
        """
        Update the grid size based on screen dimensions and tile size.
        
        :param width: screen width in pixels
        :param height: screen height in pixels
        :param tile_size: size of each cell in pixels (zoom level)
        """
        self.width = width // tile_size
        self.height = height // tile_size