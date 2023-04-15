from collections import deque
from constants import *
from direction import Direction

# the snake is controlled by the player
# the player's goal is to grow the snake
# the snake grows when it moves onto a fruit which consumes the fruit
# then a randomly selected tile will be appointed as the next fruit
class Snake:
    def __init__(self, board, start_pos: (int, int)):
        self.board = board
        self.direction = Direction.DOWN
        self.start_pos = start_pos
        self.tiles = []
        self.reset()

    # sets the direction the snake will move in on the next game tick
    def set_direction(self, direction: Direction):
        if self.direction != direction:
            destination = self.get_head_tile().get_adjacent_tile(direction)
            if len(self.tiles) == 1 or (len(self.tiles) > 1 and destination != self.tiles[-2]):
                self.direction = direction

    # retrieves the tile that holds the snake's head
    def get_head_tile(self):
        return self.tiles[-1]

    # retrieves the tile that holds the snake's tail
    def get_tail_tile(self):
        return self.tiles[0]

    # updates the snake's position
    # this returns False if the snake has moved onto itself,
    #   otherwise it returns True
    def move(self):
        head = self.get_head_tile()
        next_tile = head.get_adjacent_tile(self.direction)

        if next_tile.color == FRUIT_COLOR:
            self.tiles.append(next_tile)
            next_tile.color = SNAKE_COLOR

            max_fruits = 1 + int(self.length() / 10)
            self.board.spawn_fruit(max_fruits)
            return True

        if next_tile.color == SNAKE_COLOR:
            return False

        next_tile.color = SNAKE_COLOR
        self.tiles.popleft().color = TILE_COLOR
        self.tiles.append(next_tile)
        return True

    def length(self):
        return len(self.tiles)

    def reset(self):
        for tile in self.tiles:
            tile.color = TILE_COLOR

        start_tile = self.board.get_tile(self.start_pos[0], self.start_pos[1])
        start_tile.color = SNAKE_COLOR

        self.tiles = deque([start_tile])

