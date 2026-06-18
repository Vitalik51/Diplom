import json
import os


SAVE_FILE = "progress.json"


class Progress:
    def __init__(self):
        self.data = {
            "school": 0,
            "student": 0,
            "adult": 0,
            "programmer": 0
        }
        self.load()

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as file:
                    self.data = json.load(file)
            except:
                pass

    def save(self):
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def add_star(self, player_type):
        current = self.data.get(player_type, 0)

        if current < 3:
            self.data[player_type] = current + 1
            self.save()

    def get_stars_count(self, player_type):
        return self.data.get(player_type, 0)

    def get_stars(self, player_type):
        count = self.data.get(player_type, 0)
        return "★" * count + "☆" * (3 - count)