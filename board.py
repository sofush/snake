import random
from constants import *
from tile import Tile

class Board:
    def __init__(self, width: int, height: int):
        if width == 0 or height == 0:
            print('error: width and height of board must be at least 1')
            exit(1)

        self.width = width
        self.height = height
        self.tiles = [
            [Tile(self, x, y, TILE_COLOR) for x in range(width)]
                for y in range(height)]

    def get_tile(self, x: int, y: int) -> Tile:
        return self.tiles[y % self.height][x % self.width]

    def spawn_fruit(self, max: int = 1):
        normal_tiles = []
        fruit_tiles = []

        for row in self.tiles:
            for tile in row:
                if tile.color == TILE_COLOR:
                    normal_tiles.append(tile)
                elif tile.color == FRUIT_COLOR:
                    fruit_tiles.append(tile)

        if len(fruit_tiles) >= max:
            return

        amount_to_spawn = min(max, len(normal_tiles)) - len(fruit_tiles)

        if amount_to_spawn >= 1:
            chosen_tiles = random.sample(normal_tiles, k=amount_to_spawn)

            for tile in chosen_tiles:
                tile.color = FRUIT_COLOR

