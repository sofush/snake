#!/usr/bin/env python3
from collections import deque
import pygame as pg
from pygame import Color
from pygame.surface import Surface
from pygame.event import Event
from pygame.rect import Rect

# constants
FRUIT_COLOR = Color(255, 0, 0)
SNAKE_COLOR = Color(0, 255, 0)
TILE_COLOR = Color(50, 50, 50)
BACKGROUND_COLOR = Color(0, 0, 0, 255)
DIRECTIONS = ["up", "left", "down", "right"]
TICK_RATE = 60

# initialize
pg.init()
screen = pg.display.set_mode((720, 720))
clock = pg.time.Clock()
running = True

# a tile has a color, unique coordinate and a pointer to the board that owns the tile
# the pointer allows for easy navigation of the board through the class's `get_adjacent_tile` method
class Tile:
    def __init__(self, board, x, y, color: Color):
        self.parent = board
        self.color = color
        self.x = x
        self.y = y

    def get_adjacent_tile(self, direction):
        match direction:
            case "up":
                return board.get_tile(self.x, self.y - 1)

            case "down":
                return board.get_tile(self.x, self.y + 1)

            case "left":
                return board.get_tile(self.x - 1, self.y)

            case "right":
                return board.get_tile(self.x + 1, self.y)

# the snake is controlled by the player
# the player's goal is to grow the snake
# the snake grows when it moves onto a fruit which consumes the fruit
# then a randomly selected tile will be appointed as the next fruit
class Snake:
    def __init__(self, board, start_pos: (int, int)):
        self.board = board
        self.direction = "right"
        self.length = 1

        start_tile = self.board.get_tile(start_pos[0], start_pos[1])
        start_tile.color = SNAKE_COLOR

        self.tiles = deque([start_tile])

    # sets the direction the snake will move in on the next game tick
    def set_direction(self, direction: str):
        if direction not in DIRECTIONS:
            print(f'error: {direction} is not a valid direction')
            exit()
        elif self.direction != direction:
            print(f'debug: updating direction to {direction}')
            self.direction = direction

    # retrieves the tile that holds the snake's head
    def get_head_tile(self):
        return self.tiles[self.length - 1]

    # retrieves the tile that holds the snake's tail
    def get_tail_tile(self):
        return self.tiles[0]

    # updates the snake's position
    def move(self):
        head = self.get_head_tile()
        next_tile = head.get_adjacent_tile(self.direction)

        print(f'debug: moving to {next_tile.x}, {next_tile.y}')
        next_tile.color = SNAKE_COLOR
        self.tiles.popleft().color = TILE_COLOR
        self.tiles.append(next_tile)
        return True

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
                self.tiles[x][y] = Tile(self, x, y, TILE_COLOR)

    def get_tile(self, x, y):
        return self.tiles[x % self.width][y % self.height]

# the event handler handles pygame events and ticks
class EventHandler:
    def __init__(self, snake: Snake):
        self.tick_counter = 0
        self.snake = snake

    def handle(self, event: Event):
        if event.type == pg.QUIT:
            self.stop()
        elif event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_q:
                    self.stop()

                case pg.K_UP:
                    self.snake.set_direction("up")

                case pg.K_DOWN:
                    self.snake.set_direction("down")

                case pg.K_LEFT:
                    self.snake.set_direction("left")

                case pg.K_RIGHT:
                    self.snake.set_direction("right")

    def tick(self):
        self.tick_counter = (self.tick_counter + 1) % (TICK_RATE / 2)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    exit()

        if self.tick_counter == 0:
            if not self.snake.move():
                self.game_over()

    def stop(self):
        pg.quit()
        exit()

    def game_over(self):
        print('game over')
        self.stop()

# the painter paints the board
class Painter:
    def __init__(self, board: Board):
        self.MARGIN_PX = 2
        self.board = board
        self.tile_size = self.calculate_tile_size()

    # clears the screen
    def clear(self):
        screen.fill(BACKGROUND_COLOR)

    # draws a new frame
    def paint(self):
        self.clear()
        for x in range(self.board.width):
            for y in range(self.board.height):
                tile = self.board.get_tile(x, y)
                assert tile != None
                left = self.MARGIN_PX + (self.MARGIN_PX * tile.x) + tile.x * self.tile_size[0]
                top = self.MARGIN_PX + (self.MARGIN_PX * tile.y) + tile.y * self.tile_size[1]
                rect = Rect((left, top), (self.tile_size))
                pg.draw.rect(screen, tile.color, rect)

    def calculate_tile_size(self):
        margin_width_total = self.MARGIN_PX * (board.width + 1)
        margin_height_total = self.MARGIN_PX * (board.height + 1)

        width = screen.get_width() - margin_width_total
        height = screen.get_height() - margin_height_total

        max_tile_width = int(width / board.width)
        max_tile_height = int(height / board.height)

        size = min(max_tile_width, max_tile_height)
        return (size, size)

board = Board(15, 15)
snake = Snake(board, (5, 5))
painter = Painter(board)
event_handler = EventHandler(snake)

while running:
    for event in pg.event.get():
        event_handler.handle(event)

    event_handler.tick()
    painter.paint()
    pg.display.flip()
    clock.tick(TICK_RATE)
