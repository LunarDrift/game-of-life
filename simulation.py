import random

class LifeSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.positions = set()


    def clear(self):
        self.positions.clear()


    def gen(self, num):
        """Generate `num` amount of random positions on the grid."""
        return {
            (
                random.randrange(0, self.width),
                random.randrange(0, self.height)
            )
            for _ in range(num)
        }
    
    
    def step(self):
        """Advance the simulation by one generation."""
        self.positions = self._next_generation()

    
    def _next_generation(self):
        """Adjusts the grid based on the rules of Conway's Game of Life."""
        all_neighbors = set()  # To store all neighbors of live cells
        new_positions = set()  # To store the new positions of live cells

        # Loop through all live cells
        for pos in self.positions:
            # Get neighbors of this position
            neighbors = self.get_neighbors(pos)
            # Add these neighbors to the all_neighbors set
            all_neighbors.update(neighbors)
            # Check if neighbors are alive
            neighbors = [n for n in neighbors if n in self.positions]
            # Does this position have 2 or 3 neighbors? If so, it stays alive.
            if len(neighbors) in (2, 3):
                new_positions.add(pos)

        # Loop through all neighbors of live cells
        for pos in all_neighbors:
            # Get neighbors of this position
            neighbors = self.get_neighbors(pos)
            neighbors = [n for n in neighbors if n in self.positions]
            # If a dead cell has exactly 3 live neighbors, it becomes alive.
            if len(neighbors) == 3:
                new_positions.add(pos)
        
        return new_positions
    

    def get_neighbors(self, position):
        """Returns an array or set that contains all neighboring positions of a given position."""
        x, y = position
        neighbors = []

        # Loop through all possible neighbor offsets
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue  # This is the cell itself, not a neighbor; ignore

                # Calculate neighbor position
                nx, ny = x + dx, y + dy
                # Ensure neighbor is within grid bounds before adding
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))

        return neighbors
    

    def update_grid_size(self, width, height, tile_size):
        """
        Update the grid size based on screen dimensions and tile size.
        
        :param width: screen width in pixels
        :param height: screen height in pixels
        :param tile_size: size of each cell in pixels (zoom level)
        """
        self.width = width // tile_size
        self.height = height // tile_size