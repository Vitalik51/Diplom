class Card:
    def __init__(self, name, description, xp_reward, location, hidden_text):
        self.name = name
        self.description = description
        self.xp_reward = xp_reward
        self.location = location
        self.hidden_text = hidden_text

        self.collected = False
        self.hint_found = False
        self.task_completed = False

    def find_hint(self):
        self.hint_found = True

    def complete_task(self):
        self.task_completed = True

    def collect(self):
        if self.collected:
            return 0

        if not self.task_completed:
            return -1

        self.collected = True
        return self.xp_reward