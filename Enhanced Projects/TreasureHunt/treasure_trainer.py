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

# Try to enable ESC support
try:
    import msvcrt
    _HAS_MSVCRT = True
except ImportError:
    msvcrt = None
    _HAS_MSVCRT = False


class TreasureHuntTrainer:
    def __init__(self, maze, start=(0, 0),
                 epsilon=1.0, lr=0.001, #0.001
                 epsilon_decay=0.993, min_epsilon=0.10): ##known working decay 0.992

        if isinstance(maze, TreasureMaze):
            self.qmaze = maze
        else:
            self.qmaze = TreasureMaze(maze, start)

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.lr = lr

        self.model = None
        self.target_model = None

        self.replay_size = 5000
        self.batch_size = 64
        self.discount = 0.99
        self.train_iters_per_episode = 4
        self.target_update_steps = 10
        self.learning_step_count = 0

        self.best_steps = float('inf')
        self.experience = None

        self.input_size = None
        self.num_actions = None

        self.rows, self.cols = self.qmaze.maze.shape

        self.esc_enabled = _HAS_MSVCRT

    def _build_model(self):
        if self.input_size is None or self.num_actions is None:
            raise ValueError("input_size and num_actions must be set.")

        model = Sequential([
            Input(shape=(self.input_size,)),
            Dense(64), PReLU(),
            Dense(64), PReLU(),
            Dense(self.num_actions)
        ])
        model.compile(loss=Huber(), optimizer=Adam(learning_rate=self.lr))
        return model

    def _format_time(self, seconds):
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        else:
            return f"{seconds // 3600:.1f}h"

    def _esc_pressed(self):
        """ESC detection once per epoch."""
        if not self.esc_enabled:
            return False
        if not msvcrt.kbhit():
            return False
        key = msvcrt.getch()
        if key == b'\x1b':   # ESC key
            print("\n[ESC DETECTED] Interrupting training...")
            return True
        return False

    def train(self, n_epoch=3000, data_size=64, model_name="smart_agent", max_steps=50):
        """Main training loop (final exploitation removed)."""
        sample_state = self.qmaze.observe()
        self.input_size = sample_state.shape[0]
        self.num_actions = self.qmaze.num_actions

        if self.model is None:
            self.model = self._build_model()
            self.target_model = self._build_model()
            self.target_model.set_weights(self.model.get_weights())
            self.experience = GameExperience(max_memory=self.replay_size,
                                             discount=self.discount)

        start_time = datetime.datetime.now()
        win_history = []
        hsize = self.qmaze.maze.size

        # === Early Stopping Configuration ===
        early_stop_target = 0.90  # stop when win_rate >= 90%
        early_stop_required_epochs = 20  # must hold for this many consecutive epochs
        early_stop_counter = 0

        print(f"\nStarting training: {n_epoch} epochs, max {max_steps} steps")
        print(f"Model: {model_name} | Epsilon: {self.epsilon:.3f} → {self.min_epsilon:.3f}")
        if self.esc_enabled:
            print("ESC key: stop training, save model, return to menu.")

        try:
            for epoch in range(n_epoch):

                # === ESC check once per epoch ===
                if self._esc_pressed():
                    raise KeyboardInterrupt

                self.qmaze.reset(self.qmaze.start)
                prev_row, prev_col = self.qmaze.state
                envstate = self.qmaze.observe()

                n_steps = 0
                epoch_result = None

                # === MAIN EPISODE LOOP ===
                while True:
                    n_steps += 1

                    valid_actions = self.qmaze.valid_actions()
                    if not valid_actions:
                        reward = -0.2
                        self.experience.remember([envstate, 0, reward, envstate, True])
                        win_history.append(0)
                        epoch_result = False
                        break

                    prev_state = envstate

                    # ε-greedy
                    if np.random.rand() < self.epsilon:
                        action = random.choice(valid_actions)
                    else:
                        q_vals = self.model.predict(prev_state.reshape(1, -1), verbose=0)[0]
                        masked = np.full_like(q_vals, -np.inf)
                        for a in valid_actions:
                            masked[a] = q_vals[a]
                        action = int(np.argmax(masked))

                    # Take action
                    next_state, reward, status = self.qmaze.act(action, prev_row, prev_col)
                    done = status in ("win", "lose")
                    self.experience.remember([prev_state, action, reward, next_state, done])

                    prev_row, prev_col = self.qmaze.state

                    if status == "win":
                        epoch_result = True
                        win_history.append(1)
                        if n_steps < self.best_steps:
                            self.best_steps = n_steps
                        break

                    if n_steps >= max_steps:
                        reward = -10.0
                        self.experience.remember([prev_state, action, reward, next_state, True])
                        win_history.append(0)
                        epoch_result = False
                        break

                    envstate = next_state

                # === Experience replay training ===
                if len(self.experience.memory) >= min(data_size, self.batch_size):
                    self.experience.prepare_models_info(self.model, self.target_model)
                    for _ in range(self.train_iters_per_episode):
                        inputs, targets = self.experience.get_data(self.batch_size)
                        hist = self.model.fit(inputs, targets,
                                              epochs=1, batch_size=self.batch_size, verbose=0)
                        loss = hist.history['loss'][0]

                        self.learning_step_count += 1
                        if self.learning_step_count % self.target_update_steps == 0:
                            self.target_model.set_weights(self.model.get_weights())
                else:
                    loss = 0.0

                # === Epsilon decay ===
                self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

                win_rate = sum(win_history[-hsize:]) / max(1, len(win_history[-hsize:]))
                elapsed = self._format_time((datetime.datetime.now() - start_time).total_seconds())
                result_str = "WIN" if epoch_result else "TIMEOUT"

                print(
                    f"Epoch {epoch:03d} | {result_str:<7} | Steps: {n_steps:4d} | "
                    f"Loss: {loss:.4f} | Win Rate: {win_rate:.3f} | "
                    f"ε: {self.epsilon:.3f} | {elapsed}",
                    flush=True
                )


                # === EARLY STOPPING CHECK ===
                if win_rate >= early_stop_target:
                    early_stop_counter += 1
                else:
                    early_stop_counter = 0

                if early_stop_counter >= early_stop_required_epochs:
                    print("\nEARLY STOP TRIGGERED — Agent converged!")
                    print(f"Win rate stayed ≥ {early_stop_target:.2f} for {early_stop_required_epochs} epochs.")
                    print("Saving model and stopping training...\n")
                    self.save_model(model_name)
                    return

        except KeyboardInterrupt:
            # === ESC or Ctrl+C ===
            print("\n[TRAINING INTERRUPTED] Saving model before returning to menu...")
            self.save_model(model_name)
            print("Model saved. Returning to menu.\n")
            return

        # === TRAINING COMPLETE — AUTOMATIC SAVE ===
        self.save_model(model_name)
        return

    def save_model(self, model_name):
        os.makedirs("saved_models", exist_ok=True)
        path = os.path.join("saved_models", f"{model_name}.keras")
        self.model.save(path)
        print(f"Model saved: {path}")

    def load_model(self, model_name):
        """Load an existing model cleanly."""
        if model_name.endswith(".keras"):
            model_name = model_name[:-6]

        filepath = os.path.join("saved_models", f"{model_name}.keras")
        if not os.path.exists(filepath):
            print(f"Model '{model_name}' not found.")
            return False

        # Load main model
        self.model = load_model(filepath)

        # === FIX: determine input_size + num_actions BEFORE building target ===
        sample_state = self.qmaze.observe()
        self.input_size = sample_state.shape[0]
        self.num_actions = self.qmaze.num_actions

        # Rebuild target model properly
        self.target_model = self._build_model()
        self.target_model.set_weights(self.model.get_weights())

        # Reset replay buffer
        self.experience = GameExperience(max_memory=self.replay_size,
                                         discount=self.discount)

        print(f"Model '{model_name}' loaded successfully.")
        return True

    def play(self, start_cell=(0, 0), max_steps=None):

        if self.model is None:
            print("No model loaded.")
            return

        # Reset environment
        self.qmaze.reset(start_cell)
        envstate = self.qmaze.observe()
        step = 0

        prev_row, prev_col = self.qmaze.state

        visited_path = [self.qmaze.state]

        print(f"\nEvaluating model from start: {start_cell}")

        while True:
            step += 1

            q_vals = self.model.predict(envstate.reshape(1, -1), verbose=0)[0]
            valid = self.qmaze.valid_actions()

            if not valid:
                print("No valid moves — agent is stuck.")
                break

            masked = np.full_like(q_vals, -np.inf)
            for a in valid:
                masked[a] = q_vals[a]
            action = int(np.argmax(masked))

            # CORRECTED ACTION CALL — SAME AS TRAINING
            next_state, reward, status = self.qmaze.act(action, prev_row, prev_col)

            visited_path.append(self.qmaze.state)

            prev_row, prev_col = self.qmaze.state

            if status in ("win", "lose"):
                print(f"Game ended in {step} steps: {status.upper()}")
                break

            if max_steps is not None and step >= max_steps:
                print(f"Stopped after {max_steps} steps — TIMEOUT")
                break

            envstate = next_state

        print("Displaying final maze with path...")
        self.qmaze.show(path=visited_path)
