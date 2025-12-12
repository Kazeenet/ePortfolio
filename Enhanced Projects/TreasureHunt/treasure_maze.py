import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class TreasureMaze:
    def __init__(self, maze, start=(0, 0)):
        self.maze = np.array(maze, dtype=float)
        self.start = start
        self.reset(start)

        self.free_cells = [
            (r, c)
            for r in range(self.maze.shape[0])
            for c in range(self.maze.shape[1])
            if self.maze[r, c] == 1.0
        ]

        self.target = (self.maze.shape[0] - 1, self.maze.shape[1] - 1)
        self.num_actions = 4

    def reset(self, start=None):
        self.state = start if start is not None else self.start
        self.visited = set([self.state])
        self.visit_count = defaultdict(int)
        self.visit_count[self.state] += 1
        return self.state

    def valid_actions(self, cell=None):
        if cell is None:
            row, col = self.state
        else:
            row, col = cell

        actions = []
        nrows, ncols = self.maze.shape

        # up
        if row > 0 and self.maze[row - 1, col] == 1.0:
            actions.append(0)
        # down
        if row < nrows - 1 and self.maze[row + 1, col] == 1.0:
            actions.append(1)
        # left
        if col > 0 and self.maze[row, col - 1] == 1.0:
            actions.append(2)
        # right
        if col < ncols - 1 and self.maze[row, col + 1] == 1.0:
            actions.append(3)

        if not actions:
            return [0]  # fallback safe action

        return actions

    def act(self, action, prev_row=None, prev_col=None):
        row, col = self.state

        # Apply the action
        if action == 0:  # up
            row -= 1
        elif action == 1:  # down
            row += 1
        elif action == 2:  # left
            col -= 1
        elif action == 3:  # right
            col += 1

        nrows, ncols = self.maze.shape

        # ------------------------------------------------------------------
        # OUT-OF-BOUNDS OR WALL
        # ------------------------------------------------------------------
        if not (0 <= row < nrows and 0 <= col < ncols) or self.maze[row, col] == 0.0:
            return self.observe(), -1.0, "playing"

        # Valid move → update state
        self.state = (row, col)
        self.visit_count[self.state] += 1
        visited_before = (self.visit_count[self.state] > 1)

        # ------------------------------------------------------------------
        # Base step penalty
        # ------------------------------------------------------------------
        reward = -0.05

        # ------------------------------------------------------------------
        # Distance shaping (primary positive signal)
        # ------------------------------------------------------------------
        if prev_row is not None and prev_col is not None:
            tr, tc = self.target
            prev_dist = abs(prev_row - tr) + abs(prev_col - tc)
            new_dist = abs(row - tr) + abs(col - tc)

            if new_dist < prev_dist:
                reward += 0.2
            elif new_dist > prev_dist:
                reward -= 0.1

        # ------------------------------------------------------------------
        # Revisit penalty
        # ------------------------------------------------------------------
        if visited_before:
            reward -= 0.10

        # ------------------------------------------------------------------
        # Dead-end penalty
        # ------------------------------------------------------------------
        if len(self.valid_actions((row, col))) == 1:
            reward -= 0.15

        # ------------------------------------------------------------------
        # GOAL
        # ------------------------------------------------------------------
        if self.state == self.target:
            return self.observe(), 10.0, "win"

        return self.observe(), reward, "playing"

    def observe(self):
        r, c = self.state
        rows, cols = self.maze.shape

        # Normalize coordinates
        r_norm = 2 * r / (rows - 1) - 1  # range [-1, 1]
        c_norm = 2 * c / (cols - 1) - 1

        # Distance to target, normalized
        tr, tc = self.target
        max_dist = rows + cols
        dist_norm = (abs(r - tr) + abs(c - tc)) / max_dist

        # Action availability flags
        up_free = 1.0 if r > 0 and self.maze[r - 1, c] == 1.0 else 0.0
        down_free = 1.0 if r < rows - 1 and self.maze[r + 1, c] == 1.0 else 0.0
        left_free = 1.0 if c > 0 and self.maze[r, c - 1] == 1.0 else 0.0
        right_free = 1.0 if c < cols - 1 and self.maze[r, c + 1] == 1.0 else 0.0

        return np.array([
            r_norm, c_norm,
            dist_norm,
            up_free, down_free, left_free, right_free
        ], dtype=np.float32)

    def show(self, path=None):
        canvas = np.copy(self.maze)

        if path is not None:
            for (r, c) in path:
                if 0 <= r < self.maze.shape[0] and 0 <= c < self.maze.shape[1]:
                    canvas[r, c] = 0.6

        r, c = self.state
        canvas[r, c] = 0.3

        plt.figure(figsize=(5, 5))
        plt.imshow(canvas, cmap='gray_r', interpolation='none')
        plt.xticks([])
        plt.yticks([])
        plt.show()
