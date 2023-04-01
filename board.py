import random
from pygame.color import Color
from constants import *

# a tile has a color, unique coordinate and a pointer to the board that owns the tile
# the pointer allows for easy navigation of the board through the class's `get_adjacent_tile` method
class Tile:
    def __init__(self, board, x, y, color: Color):
        self.board = board
        self.color = color
        self.x = x
        self.y = y

    def get_adjacent_tile(self, direction):
        match direction:
            case "up":
                return self.board.get_tile(self.x, self.y - 1)

            case "down":
                return self.board.get_tile(self.x, self.y + 1)

            case "left":
                return self.board.get_tile(self.x - 1, self.y)

            case "right":
                return self.board.get_tile(self.x + 1, self.y)

# the board holds a two-dimensional array of tiles
class Board:
    def __init__(self, width, height):
        if width == 0 or height == 0:
            print("error: width and height of board must be at least 1")

        self.width = width
        self.height = height

        self.tiles = [[0 for x in range(width)] for y in range(height)]
        for x in range(width):
            for y in range(height):
                self.tiles[y][x] = Tile(self, x, y, TILE_COLOR)

    # gets a tile on the board
    # if x or y is greater than the boards width or height respectively,
    #   it wraps around the board and returns that tile instead
    def get_tile(self, x, y):
        return self.tiles[y % self.height][x % self.width]

    def spawn_fruit(self):
        normal_tiles = []
        
        for row in self.tiles:
            for tile in row:
                if tile.color == TILE_COLOR:
                    normal_tiles.append(tile)

        fruit_tile = random.choice(normal_tiles)
        fruit_tile.color = FRUIT_COLOR

