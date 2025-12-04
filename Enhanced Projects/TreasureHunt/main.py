
from treasure_trainer import TreasureHuntTrainer
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
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

    # Pass the raw maze; trainer will create TreasureMaze internally
    trainer = TreasureHuntTrainer(maze)

    while True:
        print("\n" + "=" * 40, flush=True)
        print("   TREASURE HUNT – MAIN MENU", flush=True)
        print("=" * 40, flush=True)
        print("1. Train a new model", flush=True)
        print("2. Load an existing model", flush=True)
        print("3. Play loaded model", flush=True)
        print("4. Show maze", flush=True)
        print("5. Quit", flush=True)
        print("-" * 40, flush=True)

        choice = input("Choose an option (1-5): ").strip()

        #Starts training process
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
                print("Invalid number. Using 1000.")
                n_epochs = 1000

            print(f"\nTraining '{model_name}' for {n_epochs} epochs...")
            trainer.train(
                n_epoch=n_epochs,
                model_name=model_name,
                #edit maximum steps/episodes through maze an agent can take before being timed out
                max_steps=500
            )
            print("\n" + "═" * 50)
            print("TRAINING COMPLETE!")
            print("RETURNING TO MAIN MENU...")
            print("═" * 50)
            input("Press Enter to continue...")

        #load saved model
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
                    print("  (no saved_models directory yet)")
                continue
            success = trainer.load_model(model_name)
            if success:
                print(f"Model '{model_name}' is ready to play!")

        #play loaded model
        elif choice == "3":
            if trainer.model is None:
                print("No model loaded. Train or load one first.")
                continue

            trainer.play(start_cell=(0, 0), max_steps=500)

        elif choice == "4":
            # Simple static maze visualization
            maze_array = np.array(maze, dtype=float)
            start = (0, 0)
            end = (len(maze) - 1, len(maze[0]) - 1)
            maze_array[start] = 0.5   # mark start1
            maze_array[end] = 0.7     # mark goal

            plt.figure(figsize=(7, 7))
            plt.imshow(maze_array, cmap='gray_r', interpolation='none')
            plt.title("Treasure Maze\n(White = Path, Dark = Wall, Light = Start/Goal)", fontsize=12)
            plt.xticks([]); plt.yticks([])
            plt.grid(True, which='minor', color='black', linewidth=1)
            plt.show()

        elif choice == "5":
            print("Thank you for playing Treasure Hunt!")
            print("Models are saved in: saved_models/")
            break

        else:
            print("Invalid choice. Please enter 1–5.")


if __name__ == "__main__":
    os.makedirs("saved_models", exist_ok=True)
    main()