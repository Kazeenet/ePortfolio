# Treasure Hunt– Deep Q-Learning Maze Solver

A reinforcement learning project that trains an AI agent to navigate a 2D maze using Deep Q-Networks (DQN). This neural network learns to find the treasure through trial, error, and experience.

## Overview

This program implements a complete Deep Q-Learning system where an AI agent learns to solve a 7×7 maze puzzle. The agent starts at the top-left corner and must navigate through walls and paths to reach the treasure at the bottom-right corner.

**Key Features:**
- Neural network-based Q-value approximation
- Experience replay memory for stable learning
- Target network synchronization
- Epsilon-greedy exploration strategy
- Interactive menu system for training, loading, and visualization
- Automatic model saving with early stopping

## Quick Start

### Prerequisites

```bash
pip install numpy tensorflow matplotlib
```

### Running the Program

```bash
python main.py
```

## Getting Started (For New Users)

A pre-trained model called `CONVERGED.keras` is included in the `saved_models/` directory. This model has been trained to **95% accuracy** and is ready to use immediately. Load and play the model, and you will see the path it has learned to solve the maze.

### Option 1: Use the Pre-trained Model (Recommended for First-Time Users)

1. Run `python main.py`
2. Select **Option 2: Load an Existing Model**
3. Enter the model name: `CONVERGED`
4. Select **Option 3: Play Loaded Model**
5. Watch the AI navigate the maze perfectly!

### Option 2: Train Your Own Model

1. Run `python main.py`
2. Select **Option 1: Train a New Model**
3. Enter a custom name for your model
4. Choose the number of training epochs (default: 500)
5. Wait for training to complete

**Important:** Training your own model can take **over an hour** depending on your hardware and the number of epochs chosen. Please be patient! The training process will display real-time progress including win rate, loss, and epsilon values.

**Early Stopping:** If your model reaches 95% win rate before completing all epochs, training will automatically stop and save the model.

## Menu Options

### 1. Train a New Model
- Build and train a fresh neural network from scratch
- Customize model name and training duration
- View real-time training metrics (win rate, loss, steps, rewards)
- Models automatically save when training completes or early-stop criteria are met

### 2. Load an Existing Model
- Load a previously trained `.keras` model file
- Use the included `CONVERGED` model or any model you've trained

### 3. Play Loaded Model
- Watch the AI agent navigate the maze using the loaded model
- Visualizes the complete path taken by the agent
- Shows whether the agent successfully reached the treasure

### 4. Show Maze
- Display the maze layout with walls, paths, start position, and goal

### 5. Help / Instructions
- View detailed information about the program and training process

### 6. Quit
- Exit the program (all models remain saved in `saved_models/`)

## How It Works

### Deep Q-Learning (DQN)

The agent uses a neural network to approximate Q-values for each possible action (up, down, left, right) given the current state. The system includes:

- **State Representation:** 7-dimensional vector containing:
  - Normalized agent position (row, column)
  - Normalized distance to treasure
  - Binary flags for each direction (can move or blocked)

- **Reward System:**
  - **+10.0** for reaching the treasure
  - **+0.2** for moving closer to the goal
  - **-0.1** for moving away from the goal
  - **-0.10** for revisiting a cell
  - **-0.15** for entering a dead-end
  - **-1.0** for hitting a wall
  - **-0.05** base step penalty

- **Experience Replay:** Stores up to 5,000 past experiences and randomly samples batches for training to break correlation between consecutive samples

- **Target Network:** Periodically synchronized copy of the main network that provides stable Q-value targets during training

### Training Process

1. Agent starts at position (0, 0)
2. Uses epsilon-greedy exploration (random actions early, optimal actions later)
3. Takes actions and receives rewards
4. Stores experiences in replay buffer
5. Trains neural network on random batches
6. Gradually reduces exploration (epsilon decay)
7. Updates target network periodically
8. Continues until reaching 95% win rate or completing all epochs

## Project Structure

```
treasure-hunt-dqn/
│
├── main.py                 # Main menu and program entry point
├── treasure_trainer.py     # DQN trainer with training loop
├── treasure_maze.py        # Maze environment and game logic
├── game_experience.py      # Experience replay memory
│
└── saved_models/
    └── CONVERGED.keras     # Pre-trained model (95% accuracy)
```

## Training Tips

- **Epoch Count:** Higher epoch counts generally lead to better performance. The default of 500 epochs is a good starting point.
- **Win Rate Goal:** Models performing at 95%+ win rate are considered well-trained
- **Patience:** Initial training epochs may show poor performance as the agent explores randomly
- **Hardware:** Training speed depends on your CPU/GPU. Consider starting with fewer epochs (100-200) to test.

## Understanding Training Output

```
Epoch 250 | WIN | Steps: 45/300 | Reward: 8.75 | Loss: 0.0234 | Win Rate: 0.960 | ε: 0.089 | 25m 30s
```

- **Epoch:** Current training episode
- **WIN/TIMEOUT:** Whether the agent reached the treasure
- **Steps:** Number of moves taken (lower is better)
- **Reward:** Total reward accumulated during episode
- **Loss:** Neural network training loss (lower is better)
- **Win Rate:** Success rate over last 50 episodes
- **ε (Epsilon):** Current exploration rate
- **Time:** Total elapsed training time

## Configuration

You can modify parameters in `treasure_trainer.py`:

- `epsilon`: Initial exploration rate (default: 0.9)
- `epsilon_decay`: Exploration decay rate (default: 0.99)
- `min_epsilon`: Minimum exploration rate (default: 0.05)
- `lr`: Learning rate (default: 0.001)
- `max_memory`: Experience replay buffer size (default: 5000)
- `discount`: Future reward discount factor (default: 0.95)
