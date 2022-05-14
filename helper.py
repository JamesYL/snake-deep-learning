from random import choice, random
from snake import Snake, directions
import numpy as np
TOTAL_STATES = 6
TOTAL_ACTIONS = 4


def get_random_action():
    return choice(directions)


def get_state(snake: Snake):
    food = snake.food
    head = snake.head
    immediate_tail = (-10, -10)
    if snake.tail:
        immediate_tail = snake.tail[0]
    return np.array([
        food[1] < head[1],
        food[0] < head[0],
        head[0] - 1 == immediate_tail[0],
        head[0] + 1 == immediate_tail[0],
        head[1] - 1 == immediate_tail[1],
        head[1] + 1 == immediate_tail[1]
    ])


def step(snake: Snake, action):
    old_head = snake.head
    food = snake.food
    caught_food, over, new_head, new_tail = snake.step(action)
    if caught_food:
        return 10
    elif over:
        return -100
    old_dist = abs(old_head[0] - food[0]) + abs(old_head[1] - food[1])
    new_dist = abs(new_head[0] - food[0]) + abs(new_head[1] - food[1])
    if new_dist < old_dist:
        return 1
    return -1
