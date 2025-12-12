import random
import datetime
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, PReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Input
from tensorflow.keras.losses import Huber
from treasure_maze import TreasureMaze
from game_experience import GameExperience
import os

# Enable ESC key detection on Windows terminals
try:
    import msvcrt
    _HAS_MSVCRT = True
except ImportError:
    msvcrt = None
    _HAS_MSVCRT = False


class TreasureHuntTrainer:
    """
    Deep Q-Learning trainer for the Treasure Maze environment.

    Handles:
    - Neural network creation (Q-network + target network)
    - Epsilon-greedy exploration
    - Experience replay
    - Training loop, logging, and model saving
    """

    def __init__(self, maze, start=(0, 0),
                 epsilon=0.9, lr=0.001,
                 epsilon_decay=0.99, min_epsilon=0.05):
        """
        Initialize the trainer and environment.

        Parameters:
            maze (list or TreasureMaze): Maze layout or a pre-built environment.
            start (tuple): Starting coordinates of the agent.
            epsilon (float): Initial exploration rate.
            lr (float): Learning rate for Adam optimizer.
            epsilon_decay (float): How quickly epsilon decreases.
            min_epsilon (float): Exploration floor value.
        """

        # Build or load the maze environment
        if isinstance(maze, TreasureMaze):
            self.qmaze = maze
        else:
            self.qmaze = TreasureMaze(maze, start)

        # Exploration parameters
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.lr = lr

        # Neural networks
        self.model = None           # Online Q-network
        self.target_model = None    # Target Q-network (stabilizes learning)

        # Replay buffer
        self.exp = GameExperience(max_memory=5000, discount=0.95)

    def build_model(self):
        """
        Construct a fully-connected DQN model.

        Input shape:
            7-dimensional state vector from TreasureMaze.observe()

        Returns:
            A compiled Keras model.
        """
        model = Sequential()
        model.add(Input(shape=(7,)))
        model.add(Dense(128))
        model.add(PReLU())
        model.add(Dense(128))
        model.add(PReLU())

        # Output: Q-value for each possible action
        model.add(Dense(self.qmaze.num_actions))

        # Huber loss = stable training for RL
        model.compile(optimizer=Adam(self.lr), loss=Huber())
        return model

    def update_target_model(self):
        """
        Sync the target network with the current Q-network.

        Helps stabilize training by removing oscillations.
        """
        self.target_model.set_weights(self.model.get_weights())

    def train(self, n_epoch=500, model_name="model", max_steps=300):
        """
        Main training loop for the DQN agent.

        Features:
        - Epsilon-greedy action selection
        - Mini-batch training from replay buffer
        - Periodic target network updates
        - Early stopping when win-rate reaches threshold
        """

        # Build networks fresh each training session
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()

        win_history = []
        batch_size = 32           # Samples per training step
        train_repeats = 10         # How many batches per episode
        target_update_interval = 1   # Sync model every N epochs

        print(f"Starting training: {n_epoch} epochs, initial max {max_steps} steps")
        print(f"Model: {model_name} | Epsilon: {self.epsilon:.3f} → {self.min_epsilon:.3f}")
        print("ESC key: stop training, save model, return to menu.")

        global_start = datetime.datetime.now()

        # ===============================
        #        TRAINING LOOP
        # ===============================
        for epoch in range(n_epoch):

            total_reward = 0.0
            loss = 0.0
            steps = 0

            # Reset environment at start of each episode
            self.qmaze.reset()
            envstate = self.qmaze.observe()
            status = "playing"
            done = False

            # -------------
            # PLAY EPISODE
            # -------------
            for t in range(max_steps):
                steps += 1

                prev_state = envstate.copy()
                prev_row, prev_col = self.qmaze.state
                valid_actions = self.qmaze.valid_actions()

                # Epsilon-greedy exploration
                if random.random() < self.epsilon:
                    action = random.choice(valid_actions)
                else:
                    # Predict Q-values and mask invalid actions
                    qs = self.model.predict(prev_state.reshape(1, -1), verbose=0)[0]
                    masked = np.full_like(qs, -np.inf)
                    for a in valid_actions:
                        masked[a] = qs[a]
                    action = int(np.argmax(masked))

                # Apply action to environment
                next_state, reward, status = self.qmaze.act(action, prev_row, prev_col)
                total_reward += reward
                done = (status == "win") or (t == max_steps - 1)

                # Store experience for replay
                self.exp.remember((prev_state, action, reward, next_state, done))
                envstate = next_state

                if done:
                    break

            # Record win/loss
            win_history.append(1 if status == "win" else 0)

            # --------------------------
            #      TRAIN THE MODEL
            # --------------------------
            for _ in range(train_repeats):
                X, y = self.exp.get_data(self.model, self.target_model, batch_size=batch_size)
                if len(X) == 0:
                    break
                loss = self.model.train_on_batch(X, y)

            # Epsilon decay (less exploration over time)
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

            # Periodically sync target network
            if epoch % target_update_interval == 0:
                self.update_target_model()

            # Compute win-rate over last 50 episodes
            if len(win_history) >= 50:
                win_rate = np.mean(win_history[-50:])
            else:
                win_rate = np.mean(win_history)

            # Logging
            now = datetime.datetime.now()
            elapsed = now - global_start
            elapsed_seconds = int(elapsed.total_seconds())
            mins = elapsed_seconds // 60
            secs = elapsed_seconds % 60

            print(
                f"Epoch {epoch:03d} | "
                f"{'WIN' if status == 'win' else 'TIMEOUT'} | "
                f"Steps: {steps:3d}/{max_steps} | "
                f"Reward: {total_reward:7.2f} | "
                f"Loss: {loss:0.4f} | "
                f"Win Rate: {win_rate:0.3f} | "
                f"ε: {self.epsilon:0.3f} | "
                f"{mins}m {secs:02d}s",
                flush=True
            )

            # ----------------------------
            #   EARLY STOPPING CONDITION
            # ----------------------------
            if win_rate >= 0.95 and epoch > 50:
                print(f"\nWin-rate target reached! ({win_rate:.3f}). Saving model.\n")
                os.makedirs("saved_models", exist_ok=True)
                self.model.save(os.path.join("saved_models", f"{model_name}.keras"))
                return

        # Save model at end of training
        os.makedirs("saved_models", exist_ok=True)
        self.model.save(os.path.join("saved_models", f"{model_name}.keras"))
        print("Training complete.")

    def play(self, start_cell=(0, 0), max_steps=300, render=True):
        """
        Runs the loaded model in the maze without training.
        Collects the path and renders only ONE final image.
        """

        if self.model is None:
            print("No model loaded! Load a model first.")
            return

        # Reset maze
        self.qmaze.reset(start_cell)
        envstate = self.qmaze.observe()

        print("\n=== PLAYING USING TRAINED MODEL ===")
        print(f"Start: {start_cell} | Target: {self.qmaze.target}")
        print("-----------------------------------")

        path = [self.qmaze.state]  # collect positions

        for step in range(max_steps):
            row, col = self.qmaze.state

            # Predict Q-values
            qs = self.model.predict(envstate.reshape(1, -1), verbose=0)[0]

            # Mask invalid actions
            valid_actions = self.qmaze.valid_actions()
            masked = np.full_like(qs, -np.inf)
            for a in valid_actions:
                masked[a] = qs[a]

            action = int(np.argmax(masked))

            # Apply action
            prev_row, prev_col = row, col
            next_state, reward, status = self.qmaze.act(action, prev_row, prev_col)
            envstate = next_state

            # Add to path list
            path.append(self.qmaze.state)

            if status == "win":
                print("\n WIN! Agent reached the treasure!")
                print(f"Total steps: {step}")
                break

        else:
            print("\n Timeout — Agent failed to reach the goal.")

        # Render only ONCE with full path
        if render:
            self.qmaze.show(path=path)

    def load_model(self, name):
        """
        Load a saved model and create a matching target network.
        """
        path = os.path.join("saved_models", f"{name}.keras")

        if not os.path.exists(path):
            print(f"Model not found: {path}")
            return False

        try:
            self.model = load_model(path)
            self.target_model = load_model(path)
            print(f"Loaded model '{name}' successfully.")
            return True

        except Exception as e:
            print(f"Failed to load model: {e}")
            return False
