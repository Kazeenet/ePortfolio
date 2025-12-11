import numpy as np
from collections import deque


class GameExperience:
    def __init__(self, max_memory=30000, discount=0.95):
        self.max_memory = max_memory
        self.discount = discount
        self.memory = deque(maxlen=max_memory)

    def remember(self, episode):
        s, a, r, s_next, done = episode
        self.memory.append((s.copy(), a, r, s_next.copy(), done))

    def get_data(self, model, target_model, batch_size=32):
        if len(self.memory) < batch_size:
            return [], []

        batch = []
        for _ in range(batch_size):
            batch.append(self.memory[np.random.randint(len(self.memory))])

        state_dim = model.input_shape[1]
        num_actions = model.output_shape[1]

        X = np.zeros((batch_size, state_dim))
        y = np.zeros((batch_size, num_actions))

        for i, (s, a, r, s_next, done) in enumerate(batch):
            X[i] = s
            qs = model.predict(s.reshape(1, -1), verbose=0)[0]

            if done:
                qs[a] = r
            else:
                tqs = target_model.predict(s_next.reshape(1, -1), verbose=0)[0]
                qs[a] = r + self.discount * np.max(tqs)

            y[i] = qs

        return X, y
