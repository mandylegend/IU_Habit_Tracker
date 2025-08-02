from datetime import datetime

class Habit:
    def __init__(self, name, periodicity, created_at=None, habit_id=None):
        self.id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")



    def to_tuple(self):
        return (self.name, self.periodicity, self.created_at)

    def __str__(self):
        return f"[{self.id}] {self.name} ({self.periodicity}) created on {self.created_at}"


   
        

        
