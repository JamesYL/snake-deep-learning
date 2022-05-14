import pygame
from gui import GUI
from snake import DOWN, LEFT, RIGHT, UP, Snake

head = (0, 0)
food = (1, 0)
steps = [RIGHT, RIGHT, RIGHT, RIGHT, DOWN, DOWN]
snake = Snake((head, food))
gui = GUI(snake)
gui.draw()
last = pygame.time.get_ticks()
while steps and not snake.over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    curr = pygame.time.get_ticks()
    if curr - last >= 400:
        last = curr
        snake.step(steps.pop())
        gui.draw()

pygame.quit()
exit()
