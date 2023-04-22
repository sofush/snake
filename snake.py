from collections import deque
from constants import *
from board import *
from direction import Direction
from data import DatabaseConnection

class Snake:
    def __init__(self, board: Board, start_pos: (int, int)):
        self.db = DatabaseConnection()
        self.board = board
        self.direction = Direction.DOWN
        self.start_pos = start_pos
        self.tiles = []
        self.reset(False)

    def set_direction(self, direction: Direction):
        if self.direction == direction:
            return

        destination = self.get_head_tile().get_adjacent_tile(direction)

        if len(self.tiles) == 1 or (len(self.tiles) > 1 and destination != self.tiles[-2]):
            self.direction = direction

    def get_head_tile(self) -> Tile:
        return self.tiles[-1]

    def get_tail_tile(self) -> Tile:
        return self.tiles[0]

    def move(self) -> bool:
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

    def length(self) -> int:
        return len(self.tiles)

    def reset(self, add_score: bool):
        if add_score:
            self.db.add_score(self.length() - 1)

        for tile in self.tiles:
            tile.color = TILE_COLOR

        start_tile = self.board.get_tile(self.start_pos[0], self.start_pos[1])
        start_tile.color = SNAKE_COLOR

        self.tiles = deque([start_tile])

