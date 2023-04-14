import sqlite3
from datetime import datetime
from constants import *

class Data():
    def __init__(self):
        self.database = sqlite3.connect(DATABASE_PATH)
        self.cached_highscore = None

        cursor = self.database.cursor()

        try:
            cursor.execute("""CREATE TABLE scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                date TIMESTAMP);""")
        except Exception as e:
            print(e)

        self.database.commit()

    def add_entry(self, score: int):
        now = datetime.now()
        cursor = self.database.cursor()
        
        try:
            cursor.execute("""INSERT INTO scores (score, date) VALUES (?, ?)""", (score, now))
            self.database.commit()
            self.cached_highscore = None
            print(f'added score entry with a score of {score}')
        except Exception as e:
            print(e)

    def get_highscore(self):
        if self.cached_highscore == None:
            cursor = self.database.cursor()

            try:
                cursor.execute("""SELECT MAX(score) FROM scores""")
            except Exception as e:
                print(e)

            self.cached_highscore = cursor.fetchone()[0]

        return self.cached_highscore
