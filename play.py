import pygame
from gui import GUI
from snake import Snake
import numpy as np
from model import TOTAL_STATES, get_model, get_state

trained_model = get_model()

snake = Snake()
state = get_state(snake)


gui = GUI(snake)
gui.draw()
last = pygame.time.get_ticks()
while not snake.over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    curr = pygame.time.get_ticks()
    if curr - last >= 50:
        last = curr
        state = get_state(snake).reshape(-1, TOTAL_STATES)
        scores = trained_model.predict(state)
        action = np.argmax(scores)
        print(f"LEFT: {scores[0][0]} UP: {scores[0][1]} RIGHT: {scores[0][2]} DOWN: {scores[0][3]}")
        snake.step(action)
        gui.draw()

pygame.quit()
exit()
