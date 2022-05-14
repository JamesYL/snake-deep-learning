from collections import deque
from random import randint
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3
directions = [LEFT, UP, RIGHT, DOWN]


class Snake:
    def __init__(self, head_and_food=None):
        self.width = 600
        self.height = 400
        self.block_width = 20
        self.tot_x_blocks = self.width // self.block_width
        self.tot_y_blocks = self.height // self.block_width
        self.over = False
        self.score = 0
        self.tail = deque()
        self.head = self.gen_random_coord()
        self.food = self.gen_food()

        if head_and_food:
            self.head = head_and_food[0]
            self.food = head_and_food[1]
            if self.head == self.food:
                raise Exception(
                    "Initialization failure, head and food cannot be same coord")

    def gen_food(self):
        if self.over:
            return
        curr = self.gen_random_coord()
        while curr in self.tail or curr == self.head:
            curr = self.gen_random_coord()
        return curr

    def gen_random_coord(self):
        return (randint(0, self.tot_x_blocks - 1), randint(0, self.tot_y_blocks - 1))

    def step(self, dir):
        if self.over:
            return
        if dir not in directions:
            raise Exception("Invalid direction")
        x, y = self.head
        if dir == LEFT:
            x -= 1
        elif dir == UP:
            y -= 1
        elif dir == RIGHT:
            x += 1
        elif dir == DOWN:
            y += 1

        new_head = (x, y)

        self.over = x < 0 or y < 0 or x >= self.tot_x_blocks or y >= self.tot_y_blocks or new_head in self.tail

        caught_food = False
        if self.over:
            return (caught_food, self.over, self.head, self.tail)
        if new_head == self.food:
            caught_food = True
            self.score += 1
            self.tail.appendleft(self.head)
            self.food = self.gen_food()
        elif len(self.tail) > 0:
            self.tail.pop()
            self.tail.appendleft(self.head)
        self.head = new_head
        return (caught_food, self.over, self.head, self.tail)

    def __str__(self):
        res = f"""
        Head: {self.head}
        Tail: {list(self.tail)}
        Score: {self.score}
        Over: {self.over}
        """
        if not self.over:
            res += f"Food: {self.food}"
        return res
