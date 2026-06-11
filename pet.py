class Pet:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0

    def add_xp(self, amount):
        self.xp += amount

        need_xp = self.level * 30

        if self.xp >= need_xp:
            self.xp = 0
            self.level += 1
            return True

        return False

    def get_info(self):
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "need_xp": self.level * 30
        }