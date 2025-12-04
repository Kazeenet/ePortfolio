import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class TreasureMaze:
    """
    Maze environment with stable reward shaping.

    Conventions:
    - Cell == 1.0 → free path
    - Cell == 0.0 → wall/blocked
    - Start = (0, 0) by default
    - Goal/target = bottom-right corner

    Rewards:
    - Invalid move (into wall or out of bounds): small penalty, stay in place
    - Small step cost
    - Distance-based shaping toward goal
    - First-visit bonus
    - Looping penalty
    - Goal reward
    """

    def __init__(self, maze, start=(0, 0)):
        # Convert to float array
        self.maze = np.array(maze, dtype=float)
        self.start = start
        self.reset(start)

        # Free cells are those with 1.0
        self.free_cells = [
            (r, c)
            for r in range(self.maze.shape[0])
            for c in range(self.maze.shape[1])
            if self.maze[r, c] == 1.0
        ]

        # Target is bottom-right
        self.target = (self.maze.shape[0] - 1, self.maze.shape[1] - 1)
        self.num_actions = 4  # up, down, left, right

    def reset(self, start=None):
        """Reset agent position and visitation statistics."""
        self.state = start if start is not None else self.start
        self.visited = set([self.state])
        self.visit_count = defaultdict(int)
        self.visit_count[self.state] += 1
        return self.state

    def valid_actions(self, cell=None):
        """Return list of valid actions from a cell (or from current state)."""
        if cell is None:
            row, col = self.state
        else:
            row, col = cell

        actions = []
        nrows, ncols = self.maze.shape

        # Up
        if row > 0 and self.maze[row - 1, col] == 1.0:
            actions.append(0)
        # Down
        if row < nrows - 1 and self.maze[row + 1, col] == 1.0:
            actions.append(1)
        # Left
        if col > 0 and self.maze[row, col - 1] == 1.0:
            actions.append(2)
        # Right
        if col < ncols - 1 and self.maze[row, col + 1] == 1.0:
            actions.append(3)

        return actions

    def act(self, action, prev_row=None, prev_col=None):

        row, col = self.state

        if action == 0:  # up
            row -= 1
        elif action == 1:  # down
            row += 1
        elif action == 2:  # left
            col -= 1
        elif action == 3:  # right
            col += 1

        nrows, ncols = self.maze.shape

        # Out of bounds OR into wall
        if not (0 <= row < nrows and 0 <= col < ncols) or self.maze[row, col] == 0.0:
            return self.observe(), -1.0, "playing"

        self.state = (row, col)
        self.visit_count[self.state] += 1
        self.visited.add(self.state)

        # === Reward structure ===
        # Small negative step cost: encourages shorter paths
        reward = -0.05

        # Strong loop penalty
        if self.visit_count[self.state] > 1:
            reward -= 0.3

        # Goal
        if self.state == self.target:
            return self.observe(), 5.0, "win"

        return self.observe(), reward, "playing"

    def observe(self):
        r, c = self.state
        r_norm = 2 * r / (self.maze.shape[0] - 1) - 1  # -1 to +1
        c_norm = 2 * c / (self.maze.shape[1] - 1) - 1
        return np.array([r_norm, c_norm], dtype=np.float32)


    def show(self, path=None):
        """Show the maze with optional path overlay."""
        import matplotlib.pyplot as plt

        # Maze copy
        canvas = np.copy(self.maze)

        # Path overlay
        if path is not None:
            for (r, c) in path:
                if 0 <= r < self.maze.shape[0] and 0 <= c < self.maze.shape[1]:
                    canvas[r, c] = 0.6  # gray path

        # Mark the agent's current final position
        r, c = self.state
        canvas[r, c] = 0.3

        plt.figure(figsize=(5, 5))
        plt.imshow(canvas, cmap='gray_r', interpolation='none')
        plt.title("Maze Path Trace")
        plt.xticks([]); plt.yticks([])
        plt.show()