import os
import sqlite3
from datetime import date, datetime
from constants import *
from score import Score

class DatabaseConnection():
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cached_highscore = None

        cursor = self.connection.cursor()

        try:
            cursor.execute('''CREATE TABLE scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player INTEGER,
                score INTEGER NOT NULL,
                date TEXT);''')

            cursor.execute('''CREATE TABLE players (
                name TEXT UNIQUE PRIMARY KEY,
                created_at TEXT);''')

            self.connection.commit()
        except Exception as e:
            print(e)

    def add_entry(self, score: int):
        now = date.today()
        cursor = self.connection.cursor()
        player = self.add_player()
        
        try:
            cursor.execute('''INSERT INTO scores (player, score, date) VALUES (?, ?, ?)''', (player, score, now))
            self.connection.commit()
            print(f'added score entry with a score of {score}')

            if not self.has_cache() or score > self.cached_highscore.score:
                self.cached_highscore = Score(player, score, now)
                print(f'new highscore with a score of {score}')
        except Exception as e:
            print(e)

    def get_highscore(self) -> Score:
        if self.cached_highscore == None:
            cursor = self.connection.cursor()

            try:
                cursor.execute('''SELECT player,MAX(score),date FROM scores''')
            except Exception as e:
                print(e)

            result = cursor.fetchone()
            print(f'updating cached highscore to {result}')
            self.cached_highscore = Score(result[0], result[1], result[2])

        return self.cached_highscore

    def has_cache(self) -> bool:
        if isinstance(self.cached_highscore, Score):
            if self.cached_highscore.is_valid():
                return True

        return False

    def add_player(self) -> str:
        try:
            username = os.environ['USER']
        except Exception as e:
            try:
                username = os.environ['USERNAME']
            except Exception as e:
                username = 'unknown'
            username = 'unknown'
        
        print(f'got username: {username}')
        created_at = datetime.now()
        cursor = self.connection.cursor()

        try:
            cursor.execute('''INSERT INTO players (name, created_at) VALUES (?, ?)''', (username, created_at))
            self.connection.commit()
        except Exception as e:
            print(e)

        return username

