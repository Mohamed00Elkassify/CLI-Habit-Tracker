# Core logic
import json 
from datetime import datetime

class HabitTracker:
    def __init__(self, file='data.json'):
        self.file = file
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_data(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def add_habit(self, habit):
        if habit not in self.data:
            self.data[habit] = []
            self.save_data()
            return f'Habit "{habit}" added.'
        return f'Habit "{habit}" already exists.'
    
    def mark_as_done(self, habit):
        if habit in self.data:
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in self.data[habit]:
                self.data[habit].append(today)
                self.save_data()
                return f'Habit "{habit}" marked as done for today.'
            return f'Habit "{habit}" already marked as done for today.'
        return f'Habit "{habit}" does not exist.'
    
    def remove_habit(self, habit):
        if habit in self.data:
            del self.data[habit]
            self.save_data()
            return f'Habit "{habit}" removed.'
        return f'Habit "{habit}" does not exist.'
    
    def list_habits(self):
        if not self.data:
            print('No habits found.')
            return
        for habit in self.data:
            print(f'- {habit}')

