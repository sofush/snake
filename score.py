class Score():
    def __init__(self, score: int, date: str):
        self.score = score
        self.date = date
    
    def is_none(self):
        return self.score == None or self.date == None
