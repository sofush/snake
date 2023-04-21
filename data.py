import os
import sqlite3
from datetime import date, datetime
from constants import *
from score import Score

class DatabaseConnection():
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        cursor = self.connection.cursor()

        try:
            cursor.execute('''CREATE TABLE Scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT,
                score INTEGER NOT NULL,
                date TEXT);''')

            cursor.execute('''CREATE TABLE Players (
                name TEXT UNIQUE PRIMARY KEY,
                created_at TEXT);''')

            self.connection.commit()
        except Exception as e:
            print(e)

    def add_score(self, score: int):
        now = date.today()
        cursor = self.connection.cursor()
        player = self.add_player()
        
        try:
            cursor.execute('''INSERT INTO Scores (player, score, date) VALUES (?, ?, ?)''', (player, score, now))
            self.connection.commit()
            print(f'added score with a value of {score}')
        except Exception as e:
            print(e)

    def get_highscore(self) -> Score:
        cursor = self.connection.cursor()

        try:
            cursor.execute('''SELECT player,MAX(score),date FROM Scores''')
        except Exception as e:
            print(e)

        result = cursor.fetchone()
        return Score(result[0], result[1], result[2])

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
            cursor.execute('''INSERT INTO Players (name, created_at) VALUES (?, ?)''', (username, created_at))
            self.connection.commit()
        except Exception as e:
            print(e)

        return username

