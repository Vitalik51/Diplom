from card import Card


class World:
    def __init__(self):
        self.current_world = 1
        self.max_world = 3
        self.current_location_index = 0

        self.locations = {
            1: ["Будинок", "Лісова стежка", "Старий міст"],
            2: ["Печера", "Підземне озеро", "Зал символів"],
            3: ["Місто знань", "Бібліотека", "Вежа мудрості"]
        }

        self.cards = self.create_cards()

    def create_cards(self):
        return {
            1: [
                Card("hello", "Команда привітання", 10, "Будинок", "Ти отримав картку hello."),
                Card("jump", "Команда стрибка", 10, "Лісова стежка", "Ти отримав картку jump."),
                Card("grow", "Команда досвіду", 15, "Старий міст", "Ти отримав картку grow."),
            ],
            2: [
                Card("run", "Команда руху", 15, "Печера", "Ти отримав картку run."),
                Card("think", "Команда мислення", 20, "Зал символів", "Ти отримав картку think."),
                Card("power", "Команда сили", 20, "Підземне озеро", "Ти отримав картку power."),
            ],
            3: [
                Card("logic", "Команда логіки", 25, "Місто знань", "Ти отримав картку logic."),
                Card("book", "Команда знань", 25, "Бібліотека", "Ти отримав картку book."),
                Card("final", "Фінальна команда", 30, "Вежа мудрості", "Ти отримав фінальну картку."),
            ]
    }

    def get_locations(self):
        return self.locations[self.current_world]

    def get_location(self):
        return self.get_locations()[self.current_location_index]

    def get_cards(self):
        return self.cards[self.current_world]

    def get_visible_card(self):
        for card in self.get_cards():
            if card.location == self.get_location() and not card.collected:
                return card
        return None

    def next_world(self):
        if self.current_world < self.max_world:
            self.current_world += 1
            self.current_location_index = 0
            return True
        return False

    def is_last_world(self):
        return self.current_world == self.max_world

    def get_name(self):
        names = {
            1: "Ліс навчання",
            2: "Печера команд",
            3: "Місто знань"
        }
        return names[self.current_world]