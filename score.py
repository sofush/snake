class Score():
    def __init__(self, score: int, date: str):
        self.score = score
        self.date = date
    
    def is_valid(self) -> bool:
        if not isinstance(self.score, int):
            return False

        if not isinstance(self.date, str):
            return False
        
        return True

