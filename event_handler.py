from snake import Snake
from game_state import GameState
from constants import *
from direction import Direction
from pygame.event import Event
import pygame as pg

class EventHandler:
    def __init__(self, snake: Snake):
        self.tick_counter = 0
        self.snake = snake

    def handle(self, state: GameState, event: Event) -> GameState:
        if event.type == pg.QUIT:
            return GameState.STOPPING
        elif event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_q:
                    return GameState.STOPPING

                case pg.K_UP:
                    self.snake.set_direction(Direction.UP)

                case pg.K_DOWN:
                    self.snake.set_direction(Direction.DOWN)

                case pg.K_LEFT:
                    self.snake.set_direction(Direction.LEFT)

                case pg.K_RIGHT:
                    self.snake.set_direction(Direction.RIGHT)

                case pg.K_RETURN:
                    if state == GameState.MENU:
                        return GameState.PLAYING

        return state

    def tick(self, state: GameState) -> GameState:
        self.tick_counter = (self.tick_counter + 1) % (FRAMERATE / 4)

        for event in pg.event.get():
            state = self.handle(state, event)

        if self.tick_counter == 0 and state == GameState.PLAYING:
            if self.snake.move():
                self.snake.reset(True)
                return GameState.MENU
        
        return state

