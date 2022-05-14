import pygame
from snake import Snake


class GUI:
    def __init__(self, snake: Snake):
        pygame.init()
        pygame.display.set_caption('Snake')
        self.snake = snake
        self.dis = pygame.display.set_mode((snake.width, snake.height))

    def draw(self):
        yellow = (255, 255, 102)
        black = (0, 0, 0)
        green = (0, 255, 0)
        blue = (50, 153, 213)
        self.dis.fill(blue)
        snake = self.snake
        dis = self.dis

        def get_rect(x, y):
            return [x * snake.block_width, y * snake.block_width, snake.block_width, snake.block_width]
        for x, y in snake.tail:
            pygame.draw.rect(
                dis, yellow, get_rect(x, y))
        x, y = snake.head
        pygame.draw.rect(dis, green, get_rect(x, y))
        x, y = snake.food
        pygame.draw.rect(dis, black, get_rect(x, y))
        pygame.display.update()


