from random import choice
import numpy as np
import tensorflow as tf
from snake import Snake, directions

TOTAL_STATES = 8
TOTAL_ACTIONS = 4
model_path = "./model"


def get_state(snake: Snake):
    food = snake.food
    head = snake.head
    immediate_tail = (-10, -10)
    if snake.tail:
        immediate_tail = snake.tail[0]
    return np.array([[
        food[0] < head[0],
        food[0] > head[0],
        food[1] < head[1],
        food[1] > head[1],
        head[0] - 1 == immediate_tail[0],
        head[0] + 1 == immediate_tail[0],
        head[1] - 1 == immediate_tail[1],
        head[1] + 1 == immediate_tail[1]
    ]])


def get_model():
    try:
        return tf.keras.models.load_model(model_path)
    except:
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.InputLayer(input_shape=(TOTAL_STATES,)))
        model.add(tf.keras.layers.Dense(8, activation='relu'))
        model.add(tf.keras.layers.Dense(6, activation='relu'))
        model.add(tf.keras.layers.Dense(TOTAL_ACTIONS, activation='linear'))
        model.compile(loss='mse', optimizer='adam', metrics=['mae'])
        return model


if __name__ == "__main__":
    model = get_model()

    episodes = 50
    learning_rate = 0.81
    discount = 0.96
    epsilon = 0.8
    epsilon_decay = 0.001

    rewards = []
    for i in range(episodes):
        if i % 10 == 0:
            model.save(model_path)
        print(f"Episode {i}")
        snake = Snake()
        state = get_state(snake)
        epsilon = max(0.1, epsilon - epsilon_decay)
        curr_step = 0
        while not snake.over and curr_step < 10 * i:
            if np.random.random() < epsilon:
                action = choice(directions)
            else:
                action = np.argmax(model.predict(state))

            # Calculating reward
            reward = 1
            old_head = snake.head
            food = snake.food
            caught_food, over, new_head, new_tail = snake.step(action)
            if caught_food:
                reward = 10
            elif over:
                reward = -100
            else:
                old_dist = np.linalg.norm(np.array(old_head) - np.array(food))
                new_dist = np.linalg.norm(np.array(new_head) - np.array(food))
                if old_dist < new_dist:
                    reward = -1

            new_state = get_state(snake)
            target_vector = model.predict(state)[0]
            target = reward + discount * np.max(model.predict(state))
            target_vector[action] = target_vector[action] + \
                learning_rate * (target - target_vector[action])
            target_vector = target_vector.reshape(-1, TOTAL_ACTIONS)
            model.fit(state, target_vector, verbose=0)
            state = new_state
            curr_step += 1
        rewards.append(snake.score)

    avg_rewards = []

    def get_average(values):
        return sum(values) / len(values)

    bin_size = 50
    for i in range(0, len(rewards), bin_size):
        avg_rewards.append(get_average(rewards[i:i + bin_size]))
    print(avg_rewards)

    model.save(model_path)
