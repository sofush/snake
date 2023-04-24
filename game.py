#!/usr/bin/env python3
import pygame as pg
from board import Board
from snake import Snake
from event_handler import EventHandler
from painter import Painter
from constants import *
from direction import Direction
from game_state import GameState

pg.init()
clock = pg.time.Clock()

state = GameState.MENU
board = Board(15, 15)
snake = Snake(board, start_pos = (5, 5))
painter = Painter(board, snake)
event_handler = EventHandler(snake)

board.spawn_fruit()

while state != GameState.STOPPING:
    state = event_handler.tick(state)
    painter.paint(state)
    pg.display.flip()
    clock.tick(FRAMERATE)

pg.quit()

