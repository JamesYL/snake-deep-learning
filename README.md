# Snake Reinforcement Learning

Using a neural network based reininforcement learning algorithm to play snake.
There are 8 input states, 6 neurons for the first hidden layer, 6 hidden neurons for the second hidden layer, and 4 output actions.

The state space are binary states only. Four states for where the food is relative to the snake head (above, right, below, or to the left). Four states for the direction of the snake head.

The action space consists of up, right, down, and left.

The rewards:

- 10 for catching food
- 1 for getting closer to the food
- -1 for getting further away from the food
- -100 for hitting a wall or itself

## Main files

Run `model.py` to train the neural network model. Run `play.py` to see the game running with the neural network predictions.

## Support files

`snake.py` is where the rules and movement of the snake are described. `gui.py` is used for drawing the snake on pygame.

`model` is the directory storing the neural network

## Tech stack

tensorflow, pygame, numpy, keras, matplotlib

## TODO

State should include "obstacles" so the location of the wall and tail pieces are known
