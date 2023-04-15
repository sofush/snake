import sqlite3
from datetime import date
from constants import *
from score import Score

class DatabaseConnection():
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cached_highscore = None

        cursor = self.connection.cursor()

        try:
            cursor.execute("""CREATE TABLE scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                date TIMESTAMP);""")
        except Exception as e:
            print(e)

        self.connection.commit()

    def add_entry(self, score: int):
        now = date.today()
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("""INSERT INTO scores (score, date) VALUES (?, ?)""", (score, now))
            self.connection.commit()
            print(f'added score entry with a score of {score}')

            if not self.has_cache() or score > self.cached_highscore.score:
                self.cached_highscore = Score(score, now)
                print(f'new highscore with a score of {score}')
        except Exception as e:
            print(e)

    def get_highscore(self) -> Score:
        if self.cached_highscore == None:
            cursor = self.connection.cursor()

            try:
                cursor.execute("""SELECT MAX(score),date FROM scores""")
            except Exception as e:
                print(e)

            result = cursor.fetchone()
            print(f'updating cached highscore to {result}')
            self.cached_highscore = Score(result[0], result[1])

        return self.cached_highscore

    def has_cache(self) -> bool:
        if isinstance(self.cached_highscore, Score):
            if self.cached_highscore.is_valid():
                return True

        return False

