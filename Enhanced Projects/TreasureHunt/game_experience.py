import numpy as np
import random
from collections import deque


class GameExperience(object):
    """
    Replay buffer with a vectorized get_data method that builds targets
    using the online model for Q(s) and target_model for max Q(s').

    - Uses deque for memory (auto-truncate).
    - prepare_models_info caches model references and optional shapes.
    - get_data handles both (1, N) and (N,) shaped states.
    """

    def __init__(self, max_memory=10000, discount=0.95):
        self.max_memory = max_memory
        self.discount = discount
        self.memory = deque(maxlen=self.max_memory)

        self.num_actions = None
        self.state_shape = None
        self.online_model = None
        self.target_model = None

    def remember(self, episode):
        """
        Store one transition:
            episode = (s, a, r, s_next, done)
        """
        s, a, r, s_next, done = episode
        # store copies to avoid accidental mutation
        self.memory.append((s.copy(), a, r, s_next.copy(), done))

    def sample_batch(self, batch_size):
        if not self.memory:
            raise ValueError("No memory to sample from. Call remember() first.")
        batch_size = min(len(self.memory), batch_size)
        return random.sample(list(self.memory), batch_size)

    def prepare_models_info(self, online_model, target_model):
        """
        Call once models are available to cache shapes.
        Infers num_actions from model output when possible and
        state shape from a stored sample (supports (1, N) and (N,) shapes).
        """
        self.online_model = online_model
        self.target_model = target_model

        # Try to get num_actions from model output_shape (if available)
        try:
            self.num_actions = online_model.output_shape[-1]
        except Exception:
            self.num_actions = None

        # State shape inference from first memory sample if available
        if len(self.memory) > 0:
            s0 = self.memory[0][0]
            if hasattr(s0, "ndim"):
                if s0.ndim == 2:   # (1, N)
                    self.state_shape = s0.shape[1]
                elif s0.ndim == 1: # (N,)
                    self.state_shape = s0.shape[0]
                else:
                    self.state_shape = int(np.prod(s0.shape))
            else:
                self.state_shape = None
        else:
            self.state_shape = None

    def get_data(self, batch_size=64):
        """
        Returns: inputs (batch, state_dim), targets (batch, num_actions)

        Targets built as:
            if done:
                Q(s,a) = r
            else:
                Q(s,a) = r + discount * max_a' Q_target(s', a')
        other Q(s,·) stay as predicted by the online model.
        """
        if not self.memory:
            raise ValueError("No memory to sample from. Call remember() first.")
        if self.online_model is None or self.target_model is None:
            raise ValueError("Call prepare_models_info(online_model, target_model) first.")

        samples = self.sample_batch(batch_size)
        batch = len(samples)

        # Determine state dimension from stored samples
        s0 = samples[0][0]
        if hasattr(s0, "ndim"):
            if s0.ndim == 2:
                state_dim = s0.shape[1]
            elif s0.ndim == 1:
                state_dim = s0.shape[0]
            else:
                state_dim = int(np.prod(s0.shape))
        else:
            if self.state_shape is None:
                raise ValueError("Unable to infer state dimension.")
            state_dim = self.state_shape

        inputs = np.zeros((batch, state_dim), dtype=np.float32)
        next_inputs = np.zeros((batch, state_dim), dtype=np.float32)
        actions = np.zeros(batch, dtype=int)
        rewards = np.zeros(batch, dtype=np.float32)
        dones = np.zeros(batch, dtype=bool)

        for i, (s, a, r, s_next, done) in enumerate(samples):
            # s and s_next may be (1, N) or (N,)
            if hasattr(s, "ndim") and s.ndim == 2:
                inputs[i] = s[0]
            else:
                inputs[i] = s

            if hasattr(s_next, "ndim") and s_next.ndim == 2:
                next_inputs[i] = s_next[0]
            else:
                next_inputs[i] = s_next

            actions[i] = a
            rewards[i] = r
            dones[i] = done

        # Batch predictions
        q_values = self.online_model.predict(inputs, verbose=0)          # (batch, num_actions)
        q_next_values = self.target_model.predict(next_inputs, verbose=0)  # (batch, num_actions)
        q_next_max = np.max(q_next_values, axis=1)

        targets = q_values.copy()

        for i in range(batch):
            if dones[i]:
                targets[i, actions[i]] = rewards[i]
            else:
                targets[i, actions[i]] = rewards[i] + self.discount * q_next_max[i]

        return inputs, targets