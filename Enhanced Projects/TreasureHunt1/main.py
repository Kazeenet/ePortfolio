"""
========================================
    TREASURE HUNT – DEEP Q-LEARNING
========================================

Author: Morgan Tyler Kazee
Date:   2025-12-10
Version: 1.0.0

Description:
    This program implements a Deep Q-Learning (DQN) agent that navigates a
    2D maze environment to find a treasure. The system includes:
        • Neural-network based Q-value approximation
        • Experience replay memory
        • Target network synchronization
        • Epsilon-greedy exploration
        • Train, load, and play interactive menu system

    The user can train a new model, load an existing model, visualize the maze,
    or watch the agent navigate it. Models are saved automatically when training
    completes or early-stop criteria are met.
"""
from treasure_trainer import TreasureHuntTrainer
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
    # 7x7 block defines maze
    # 0 = wall, 1 = path
    maze = [
        [1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1],
    ]

    trainer = TreasureHuntTrainer(maze)

    while True:
        print("\n" + "=" * 40, flush=True)
        print("        TREASURE HUNT – MAIN MENU", flush=True)
        print("=" * 40, flush=True)
        print("1. Train a New Model", flush=True)
        print("2. Load an Existing Model", flush=True)
        print("3. Play Loaded Model", flush=True)
        print("4. Show Maze", flush=True)
        print("5. Help / Instructions", flush=True)
        print("6. Quit", flush=True)
        print("-" * 40, flush=True)

        choice = input("Choose an option (1–6): ").strip()

        # TRAIN NEW MODEL
        if choice == "1":
            model_name = input("Enter the name of your model: ").strip()
            if not model_name:
                print("Name cannot be empty.")
                continue

            epochs_input = input("Number of epochs (default 500): ").strip()
            try:
                n_epochs = int(epochs_input) if epochs_input.isdigit() else 500
                if n_epochs < 1:
                    raise ValueError
            except Exception:
                print("Invalid number. Using 500.")
                n_epochs = 500

            print(f"\nTraining '{model_name}' for {n_epochs} epochs...")
            trainer.train(
                n_epoch=n_epochs,
                model_name=model_name,
                max_steps=300
            )
            print("\n" + "═" * 50)
            print("TRAINING COMPLETE!")
            print("RETURNING TO MAIN MENU...")
            print("═" * 50)
            input("Press Enter to continue...")

        # LOAD MODEL
        elif choice == "2":
            model_name = input("Enter model name to load: ").strip()
            filepath = os.path.join("saved_models", f"{model_name}.keras")

            if not os.path.exists(filepath):
                print(f"Model file not found: {filepath}")
                print("Available models:")
                if os.path.exists("saved_models"):
                    models = [f for f in os.listdir("saved_models") if f.endswith(".keras")]
                    for m in models:
                        print(f"  - {m}")
                else:
                    print("(No saved_models directory yet)")
                continue

            success = trainer.load_model(model_name)
            if success:
                print(f"Model '{model_name}' is ready to play!")

        # PLAY MODEL
        elif choice == "3":
            if trainer.model is None:
                print("No model loaded. Train or load one first.")
                continue

            trainer.play(start_cell=(0, 0), max_steps=300)

        # SHOW MAZE
        elif choice == "4":
            maze_array = np.array(maze, dtype=float)
            start = (0, 0)
            end = (len(maze) - 1, len(maze[0]) - 1)
            maze_array[start] = 0.5
            maze_array[end] = 0.7

            plt.figure(figsize=(7, 7))
            plt.imshow(maze_array, cmap='gray_r', interpolation='none')
            plt.title("Treasure Maze\n(White = Wall, Black = Path, Light Grey = Start, Dark Grey = Goal)", fontsize=12)
            plt.xticks([])
            plt.yticks([])
            plt.grid(True, which='minor', color='black', linewidth=1)
            plt.show()

        # HELP OPTION
        elif choice == "5":
            show_help()
            input("\nPress Enter to return to the main menu...")

        # QUIT OPTION
        elif choice == "6":
            print("Thank you for playing Treasure Hunt!")
            print("Models are saved in: saved_models/")
            break

        else:
            print("Invalid choice. Please enter 1–6.")

def show_help():
    print("\n" + "=" * 50)
    print("               TREASURE HUNT – HELP MENU")
    print("=" * 50)

    print("""
SUMMARY
----------------------------------------
Treasure Hunt is a reinforcement learning game where an AI agent learns
to navigate a maze using a Deep Q-Learning (DQN) neural network.
The agent trains through repeated episodes, improving its strategy
based on rewards and penalties.

MENU OPTIONS
----------------------------------------
1. TRAIN A NEW MODEL
   - Builds and trains a new neural network.
   - You will be asked for a model name and number of training epochs.
   - Training logs show win/loss results, steps taken, reward totals,
     loss values, and current win rate.
   - The model automatically saves when training ends.
   - If the model reaches a 95% win rate before completing all training epochs 
     the early stop function will automatically end training, save model, 
     and return to main menu.
     
2. LOAD AN EXISTING MODEL
   - Loads a previously trained .keras model file.
   - You must have run training at least once to have saved models.

3. PLAY LOADED MODEL
   - Shows the path the currently loaded model has taken.

4. SHOW MAZE
   - Displays a map of the maze layout: walls, paths, start, and goal.

5. HELP / INSTRUCTIONS
   - Shows this help guide.

6. QUIT
   - Exits the program. All saved models remain in saved_models/.

TRAINING TIPS
----------------------------------------
• Higher epoch counts lead to better learning.
• Good models eventually achieve over 95% win rate.
• The agent receives:
    - Penalties for walking into walls or looping.
    - Rewards for moving closer to the goal.
    - A large reward for reaching the treasure.
• Model performance improves as the neural network learns the maze.

SAVED MODEL LOCATION
----------------------------------------
All trained models are stored in:
    saved_models/<your_model>.keras

Enjoy exploring machine learning with Treasure Hunt!
""")

    print("=" * 50)

if __name__ == "__main__":
    os.makedirs("saved_models", exist_ok=True)
    main()