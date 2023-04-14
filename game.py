#!/usr/bin/env python3
from enum import Enum
import pygame as pg
from pygame import Color
from pygame.surface import Surface
from pygame.event import Event
from pygame.rect import Rect
from board import Tile, Board
from player import Snake
from constants import *
from data import Data

# initialize
pg.init()
pg.font.init()
font = pg.font.Font(size=32)
font.set_bold(True)
screen = pg.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT))
clock = pg.time.Clock()

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    EXITING = 3

state = GameState.MENU
data = Data()

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
                    self.snake.set_direction('up')

                case pg.K_DOWN:
                    self.snake.set_direction('down')

                case pg.K_LEFT:
                    self.snake.set_direction('left')

                case pg.K_RIGHT:
                    self.snake.set_direction('right')

                case pg.K_RETURN:
                    global state
                    if state == GameState.MENU:
                        state = GameState.PLAYING

    def tick(self):
        global state
        self.tick_counter = (self.tick_counter + 1) % (FRAMERATE / 4)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                state = GameState.EXITING
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.stop()

        if self.tick_counter == 0 and state == GameState.PLAYING:
            if not self.snake.move():
                self.game_over()

    def stop(self):
        global state
        state = GameState.EXITING

    def game_over(self):
        global state, data
        data.add_entry(self.snake.length() - 1)
        state = GameState.MENU
        self.snake.reset()

# the painter paints the board
class Painter:
    def __init__(self, board: Board, snake: Snake):
        self.snake = snake
        self.board = board
        self.tile_size = self.calculate_tile_size()

    # clears the screen
    def clear(self):
        screen.fill(BACKGROUND_COLOR)

    # draws a new frame
    def paint(self):
        global data
        self.clear()

        if state == GameState.PLAYING:
            for x in range(self.board.width):
                for y in range(self.board.height):
                    tile = self.board.get_tile(x, y)
                    assert tile != None
                    left = MARGIN_PX + (MARGIN_PX * tile.x) + tile.x * self.tile_size[0]
                    top = MARGIN_PX + (MARGIN_PX * tile.y) + tile.y * self.tile_size[1]
                    rect = Rect((left, top), (self.tile_size))
                    pg.draw.rect(screen, tile.color, rect)

            score_surface = font.render(f'Score: {self.snake.length() - 1}', True, FONT_COLOR)
            screen.blit(score_surface, (10, 10))
        elif state == GameState.MENU:
            center_width = DEFAULT_SCREEN_WIDTH / 2
            center_height = DEFAULT_SCREEN_HEIGHT / 2

            instruction_str = 'PRESS ENTER TO PLAY'
            instruction_text = font.render(instruction_str, True, FONT_COLOR)
            instruction_height_offset = -(instruction_text.get_height())
            instruction_pos = (center_width, center_height + instruction_height_offset)

            highscore = data.get_highscore()
            highscore_str = f'HIGHSCORE: {highscore}'
            highscore_text = font.render(highscore_str, True, FONT_COLOR)
            highscore_height_offset = highscore_text.get_height()
            highscore_pos = (center_width, center_height + highscore_height_offset)

            instruction_rect = instruction_text.get_rect(center=instruction_pos)
            highscore_rect = highscore_text.get_rect(center=highscore_pos)

            screen.blit(instruction_text, instruction_rect)
            screen.blit(highscore_text, highscore_rect)

    def calculate_tile_size(self):
        margin_width_total = MARGIN_PX * (board.width + 1)
        margin_height_total = MARGIN_PX * (board.height + 1)

        width = screen.get_width() - margin_width_total
        height = screen.get_height() - margin_height_total

        max_tile_width = int(width / board.width)
        max_tile_height = int(height / board.height)

        size = min(max_tile_width, max_tile_height)
        return (size, size)

board = Board(15, 15)
snake = Snake(board, start_pos = (5, 5))
painter = Painter(board, snake)
event_handler = EventHandler(snake)

board.spawn_fruit()

while state != GameState.EXITING:
    for event in pg.event.get():
        event_handler.handle(event)

    event_handler.tick()
    painter.paint()
    pg.display.flip()
    clock.tick(FRAMERATE)

pg.quit()

