#!/usr/bin/env python3
import pygame as pg
from pygame import Color
from pygame.surface import Surface
from pygame.event import Event
from pygame.rect import Rect
from board import Tile, Board
from player import Snake
from constants import *

# initialize
pg.init()
screen = pg.display.set_mode((720, 720))
clock = pg.time.Clock()
running = True

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
        self.tick_counter = (self.tick_counter + 1) % (FRAMERATE / 4)
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
snake = Snake(board, start_pos = (5, 5))
painter = Painter(board)
event_handler = EventHandler(snake)

board.spawn_fruit()

while running:
    for event in pg.event.get():
        event_handler.handle(event)

    event_handler.tick()
    painter.paint()
    pg.display.flip()
    clock.tick(FRAMERATE)

