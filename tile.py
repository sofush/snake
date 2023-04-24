from direction import Direction
from pygame.color import Color

class Tile:
    def __init__(self, board, x: int, y: int, color: Color):
        self.board = board
        self.color = color
        self.x = x
        self.y = y

    def get_adjacent_tile(self, direction: Direction):
        match direction:
            case Direction.UP:
                return self.board.get_tile(self.x, self.y - 1)

            case Direction.DOWN:
                return self.board.get_tile(self.x, self.y + 1)

            case Direction.LEFT:
                return self.board.get_tile(self.x - 1, self.y)

            case Direction.RIGHT:
                return self.board.get_tile(self.x + 1, self.y)

