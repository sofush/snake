from board import Board
from snake import Snake
from game_state import GameState
from constants import *
from pygame.rect import Rect
import pygame as pg

pg.font.init()
font = pg.font.Font(size=32)
font.set_bold(True)

class Painter:
    def __init__(self, board: Board, snake: Snake):
        self.snake = snake
        self.board = board
        self.screen = pg.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT))
        self.tile_size = self.calculate_tile_size()

    def clear(self):
        self.screen.fill(BACKGROUND_COLOR)

    def paint(self, state: GameState):
        self.clear()

        if state == GameState.PLAYING:
            for x in range(self.board.width):
                for y in range(self.board.height):
                    tile = self.board.get_tile(x, y)
                    assert tile != None
                    left = MARGIN_PX + (MARGIN_PX * tile.x) + tile.x * self.tile_size[0]
                    top = MARGIN_PX + (MARGIN_PX * tile.y) + tile.y * self.tile_size[1]
                    rect = Rect((left, top), (self.tile_size))
                    pg.draw.rect(self.screen, tile.color, rect)

            score_surface = font.render(f'Score: {self.snake.length() - 1}', True, FONT_COLOR)
            self.screen.blit(score_surface, (10, 10))
        elif state == GameState.MENU:
            center_width = DEFAULT_SCREEN_WIDTH / 2
            center_height = DEFAULT_SCREEN_HEIGHT / 2

            instruction_str = 'PRESS ENTER TO PLAY'
            instruction_text = font.render(instruction_str, True, FONT_COLOR)
            instruction_height_offset = -(instruction_text.get_height())
            instruction_pos = (center_width, center_height + instruction_height_offset)

            highscore = self.snake.db.get_highscore()
            highscore_str = f'HIGHSCORE ({highscore.date} by {highscore.player}): {highscore.score}'
            highscore_text = font.render(highscore_str, True, FONT_COLOR)
            highscore_height_offset = highscore_text.get_height()
            highscore_pos = (center_width, center_height + highscore_height_offset)

            instruction_rect = instruction_text.get_rect(center=instruction_pos)
            highscore_rect = highscore_text.get_rect(center=highscore_pos)

            self.screen.blit(instruction_text, instruction_rect)

            if highscore.date != None:
                self.screen.blit(highscore_text, highscore_rect)

    def calculate_tile_size(self) -> (int, int):
        margin_width_total = MARGIN_PX * (self.board.width + 1)
        margin_height_total = MARGIN_PX * (self.board.height + 1)

        width = self.screen.get_width() - margin_width_total
        height = self.screen.get_height() - margin_height_total

        max_tile_width = int(width / self.board.width)
        max_tile_height = int(height / self.board.height)

        size = min(max_tile_width, max_tile_height)
        return (size, size)

