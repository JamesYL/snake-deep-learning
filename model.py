import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import Dense

from helper import TOTAL_ACTIONS, TOTAL_STATES, get_random_action, get_state, step
from snake import Snake

model = Sequential()
model.add(InputLayer(input_shape=(TOTAL_STATES,)))
model.add(Dense(20, activation='relu'))
model.add(Dense(TOTAL_ACTIONS, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])


episodes = 1500
max_steps = 100
learning_rate = 0.81
discount = 0.96
epsilon = 0.9
epsilon_decay_factor = 0.999

rewards = []
for i in range(episodes):
    snake = Snake()
    state = get_state(snake)
    epsilon *= epsilon_decay_factor

    curr_step = 0
    while not snake.over and curr_step < max_steps:
        if np.random.random() < epsilon:
            action = get_random_action()
        else:
            action = np.argmax(model.predict(state.reshape(-1, TOTAL_STATES)))
        reward = step(snake, action)
        new_state = get_state(snake)
        target_vector = model.predict(state.reshape(-1, TOTAL_STATES))[0]

        target = reward + discount * \
            np.max(model.predict(new_state.reshape(-1, TOTAL_STATES)))
        target_vector[action] += learning_rate * target
        model.fit(state.reshape(-1, TOTAL_STATES), target_vector.reshape(-1, TOTAL_ACTIONS))
        state = new_state
        curr_step += 1
    rewards.append(snake.score)

avg_rewards = []
def get_average(values):
    return sum(values) / len(values)
for i in range(0, len(rewards), 100):
    avg_rewards.append(get_average(rewards[i:i + 100]))
print(avg_rewards)
