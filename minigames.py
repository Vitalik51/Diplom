import random
import pygame
from settings import *

DIFFICULTY_SETTINGS = {
    "easy":   {"label": "Легко",    "time": 60000, "goal": 10, "color": (60, 220, 90)},
    "medium": {"label": "Середній", "time": 40000, "goal": 10, "color": (230, 180, 30)},
    "hard":   {"label": "Важко",    "time": 25000, "goal": 10, "color": (220, 60, 60)},
}


class MiniGames:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 26)
        self.big_font = pygame.font.SysFont("arial", 38)
        self.small_font = pygame.font.SysFont("arial", 20)

        self.active_game = None
        self.input_text = ""
        self.message = "Оберіть мінігру"
        self.score = 0
        self.current_question = None
        self.target_number = None
        self.memory_word = None
        self.show_word_until = 0

        self.math_difficulty = None     
        self.math_time_limit = 30000
        self.math_goal = 10
        self.math_start_time = 0
        self.math_game_over = False
        self.math_final_score = 0
        self.math_won = False

        self.buttons = {}



    def draw_button(self, rect, text, color_override=None):
        mouse = pygame.mouse.get_pos()
        if color_override:
            base = tuple(min(255, c + 30) for c in color_override) if rect.collidepoint(mouse) else color_override
        else:
            base = BUTTON_HOVER if rect.collidepoint(mouse) else BUTTON

        pygame.draw.rect(self.screen, base, rect, border_radius=12)
        pygame.draw.rect(self.screen, YELLOW, rect, 2, border_radius=12)

        img = self.font.render(text, True, WHITE)
        self.screen.blit(img, img.get_rect(center=rect.center))


    def draw_menu(self):
        self.screen.fill((12, 16, 28))

        title = self.big_font.render("Мініігри", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))

        subtitle = self.small_font.render(
            "Тут потрібно вводити відповіді вручну з клавіатури",
            True, TEXT_MUTED
        )
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 135)))

        self.buttons = {
            "number": pygame.Rect(WIDTH // 2 - 170, 210, 340, 55),
            "math":   pygame.Rect(WIDTH // 2 - 170, 285, 340, 55),
            "memory": pygame.Rect(WIDTH // 2 - 170, 360, 340, 55),
            "back":   pygame.Rect(WIDTH // 2 - 170, 470, 340, 55),
        }

        self.draw_button(self.buttons["number"], "Вгадай число")
        self.draw_button(self.buttons["math"],   "Математичний спринт")
        self.draw_button(self.buttons["memory"], "Пам'ять")
        self.draw_button(self.buttons["back"],   "Назад")

    def draw_difficulty_menu(self):
        """Екран вибору складності перед математичним спринтом."""
        self.screen.fill((12, 16, 28))

        title = self.big_font.render("Математичний спринт", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 75)))

        subtitle = self.font.render("Оберіть рівень складності", True, WHITE)
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 130)))

        card_data = [
            ("easy",   "Легко",    "60 сек  •  ціль 10 балів", 200),
            ("medium", "Середній", "40 сек  •  ціль 10 балів", 290),
            ("hard",   "Важко",    "25 сек  •  ціль 10 балів", 380),
        ]

        self.buttons = {"back": pygame.Rect(WIDTH // 2 - 170, 475, 340, 50)}

        for key, label, desc, y in card_data:
            cfg = DIFFICULTY_SETTINGS[key]
            card = pygame.Rect(WIDTH // 2 - 200, y, 400, 70)
            mouse = pygame.mouse.get_pos()
            bg = tuple(min(255, c + 20) for c in cfg["color"]) if card.collidepoint(mouse) else tuple(max(0, c - 80) for c in cfg["color"])
            pygame.draw.rect(self.screen, bg, card, border_radius=14)
            pygame.draw.rect(self.screen, cfg["color"], card, 2, border_radius=14)

            lbl = self.font.render(label, True, WHITE)
            self.screen.blit(lbl, (card.x + 20, card.y + 10))

            dsc = self.small_font.render(desc, True, WHITE)
            self.screen.blit(dsc, (card.x + 20, card.y + 40))

            self.buttons[key] = card

        self.draw_button(self.buttons["back"], "Назад")

    def start_number_game(self):
        self.active_game = "number"
        self.target_number = random.randint(1, 20)
        self.input_text = ""
        self.message = "Я загадав число від 1 до 20. Введи відповідь."
        self.score = 0

    def start_math_difficulty_select(self):
        """Переходимо до екрану вибору складності."""
        self.active_game = "math_difficulty"
        self.math_difficulty = None

    def start_math_game(self, difficulty):
        cfg = DIFFICULTY_SETTINGS[difficulty]
        self.active_game = "math"
        self.math_difficulty = difficulty
        self.math_time_limit = cfg["time"]
        self.math_goal = cfg["goal"]
        self.score = 0
        self.input_text = ""
        self.math_start_time = pygame.time.get_ticks()
        self.math_game_over = False
        self.math_won = False
        self.math_final_score = 0
        self.generate_math_question()

    def start_memory_game(self):
        self.active_game = "memory"
        self.input_text = ""
        words = ["КІТ", "ЛІС", "МІСТ", "КНИГА", "ПЕЧЕРА", "ЗІРКА", "КОМАНДА"]
        self.memory_word = random.choice(words)
        self.show_word_until = pygame.time.get_ticks() + 1000
        self.message = "Запам'ятай слово, потім введи його з клавіатури."


    def generate_math_question(self):
        a = random.randint(5, 30)
        b = random.randint(2, 20)
        op = random.choice(["+", "-", "*"])

        correct = a + b if op == "+" else (a - b if op == "-" else a * b)

        self.current_question = {"text": f"{a} {op} {b} = ?", "answer": str(correct)}
        self.message = "Введи правильну відповідь."

    def get_math_time_left(self):
        elapsed = pygame.time.get_ticks() - self.math_start_time
        return max(0, self.math_time_limit - elapsed)


    def draw_timer_bar(self):
        time_left = self.get_math_time_left()
        ratio = time_left / self.math_time_limit

        bar_w, bar_h = 360, 18
        bar_x = WIDTH // 2 - bar_w // 2
        bar_y = 185

        pygame.draw.rect(self.screen, (40, 40, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=9)

        bar_color = (60, 220, 90) if ratio > 0.5 else ((230, 180, 30) if ratio > 0.25 else (220, 60, 60))
        fill_w = int(bar_w * ratio)
        if fill_w > 0:
            pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, fill_w, bar_h), border_radius=9)

        pygame.draw.rect(self.screen, YELLOW, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=9)

        secs = (time_left + 999) // 1000
        label = self.small_font.render(f"{secs}с", True, WHITE)
        self.screen.blit(label, (bar_x + bar_w + 10, bar_y - 1))

    def draw_goal_progress(self):
        """Маленький індикатор прогресу до цілі."""
        text = self.small_font.render(f"Ціль: {self.score}/{self.math_goal}", True, WHITE)
        self.screen.blit(text, text.get_rect(topright=(WIDTH - 30, 30)))

    def draw_input_box(self):
        box = pygame.Rect(WIDTH // 2 - 180, 400, 360, 55)
        pygame.draw.rect(self.screen, (25, 30, 45), box, border_radius=10)
        pygame.draw.rect(self.screen, YELLOW, box, 2, border_radius=10)
        text = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(text, (box.x + 18, box.y + 14))

    def draw_math_result(self):
        """Екран результату (перемога або поразка)."""
        self.screen.fill((12, 16, 28))

        if self.math_won:
            cfg = DIFFICULTY_SETTINGS[self.math_difficulty]
            title_text = "Перемога!"
            title_color = cfg["color"]
            time_left = self.get_math_time_left()
            secs = time_left // 1000
            sub = self.font.render(f"Ти набрав {self.math_goal} балів! Залишилось {secs}с", True, WHITE)
        else:
            title_text = "Час вийшов!"
            title_color = (220, 60, 60)
            sub = self.font.render(f"Правильних відповідей: {self.math_final_score} / {self.math_goal}", True, WHITE)

        title = self.big_font.render(title_text, True, title_color)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 230)))

        if self.math_won:
            comment_text = "Чудово! Спробуй складніший рівень."
            comment_color = (60, 220, 90)
        elif self.math_final_score >= self.math_goal * 0.7:
            comment_text = "Майже! Ще трохи і впораєшся."
            comment_color = (230, 180, 30)
        else:
            comment_text = "Тренуйся більше!"
            comment_color = (220, 100, 60)

        comment = self.font.render(comment_text, True, comment_color)
        self.screen.blit(comment, comment.get_rect(center=(WIDTH // 2, 300)))

        self.buttons = {
            "retry": pygame.Rect(WIDTH // 2 - 170, 370, 340, 55),
            "change": pygame.Rect(WIDTH // 2 - 170, 440, 340, 55),
            "back":  pygame.Rect(WIDTH // 2 - 170, 510, 340, 55),
        }
        self.draw_button(self.buttons["retry"],  "Грати знову")
        self.draw_button(self.buttons["change"], "Змінити складність")
        self.draw_button(self.buttons["back"],   "Назад")


    def draw_game(self):
        if self.active_game == "math" and self.math_game_over:
            self.draw_math_result()
            return

        self.screen.fill((12, 16, 28))

        title = self.big_font.render("Мінігра", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

        msg = self.font.render(self.message, True, WHITE)
        self.screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 145)))

        if self.active_game == "number":
            hint = self.font.render("Введи число та натисни Enter", True, TEXT_MUTED)
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 240)))

        elif self.active_game == "math":
            if self.get_math_time_left() == 0:
                self.math_game_over = True
                self.math_final_score = self.score
                self.math_won = False
                return

            self.draw_timer_bar()
            self.draw_goal_progress()

            cfg = DIFFICULTY_SETTINGS[self.math_difficulty]
            diff_label = self.small_font.render(cfg["label"], True, cfg["color"])
            self.screen.blit(diff_label, (30, 30))

            q = self.big_font.render(self.current_question["text"], True, WHITE)
            self.screen.blit(q, q.get_rect(center=(WIDTH // 2, 270)))

        elif self.active_game == "memory":
            now = pygame.time.get_ticks()
            if now < self.show_word_until:
                word = self.big_font.render(self.memory_word, True, YELLOW)
                self.screen.blit(word, word.get_rect(center=(WIDTH // 2, 250)))
            else:
                hint = self.font.render("Введи слово, яке було показано", True, TEXT_MUTED)
                self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 250)))

        self.draw_input_box()

        score_text = self.small_font.render(f"Рахунок: {self.score}", True, WHITE)
        self.screen.blit(score_text, (30, 30))

        self.buttons = {"back": pygame.Rect(WIDTH // 2 - 120, 520, 240, 50)}
        self.draw_button(self.buttons["back"], "Назад")


    def handle_click(self, pos):
        if self.active_game is None:
            menu_buttons = {
                "number": pygame.Rect(WIDTH // 2 - 170, 210, 340, 55),
                "math":   pygame.Rect(WIDTH // 2 - 170, 285, 340, 55),
                "memory": pygame.Rect(WIDTH // 2 - 170, 360, 340, 55),
                "back":   pygame.Rect(WIDTH // 2 - 170, 470, 340, 55),
            }
            if menu_buttons["number"].collidepoint(pos):
                self.start_number_game(); return None
            if menu_buttons["math"].collidepoint(pos):
                self.start_math_difficulty_select(); return None
            if menu_buttons["memory"].collidepoint(pos):
                self.start_memory_game(); return None
            if menu_buttons["back"].collidepoint(pos):
                return "back"
            return None

        if self.active_game == "math_difficulty":
            for key in ("easy", "medium", "hard"):
                if self.buttons.get(key) and self.buttons[key].collidepoint(pos):
                    self.start_math_game(key); return None
            if self.buttons.get("back") and self.buttons["back"].collidepoint(pos):
                self.active_game = None
                self.message = "Оберіть мінігру"
            return None

        if self.active_game == "math" and self.math_game_over:
            if self.buttons.get("retry") and self.buttons["retry"].collidepoint(pos):
                self.start_math_game(self.math_difficulty); return None
            if self.buttons.get("change") and self.buttons["change"].collidepoint(pos):
                self.start_math_difficulty_select(); return None
            if self.buttons.get("back") and self.buttons["back"].collidepoint(pos):
                self.active_game = None
                self.input_text = ""
                self.message = "Оберіть мінігру"
            return None

        if self.buttons.get("back") and self.buttons["back"].collidepoint(pos):
            self.active_game = None
            self.input_text = ""
            self.message = "Оберіть мінігру"

        return None

    def handle_keydown(self, event):
        if self.active_game in (None, "math_difficulty"):
            return
        if self.active_game == "math" and self.math_game_over:
            return

        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.check_input()
        else:
            if event.unicode:
                self.input_text += event.unicode

    def check_input(self):
        answer = self.input_text.strip()

        if self.active_game == "number":
            if answer == str(self.target_number):
                self.score += 1
                self.message = "Правильно! Я загадав нове число."
                self.target_number = random.randint(1, 20)
            else:
                self.message = "Неправильно. Спробуй ще раз."

        elif self.active_game == "math":
            if self.get_math_time_left() == 0:
                return
            if answer == self.current_question["answer"]:
                self.score += 1
                self.message = "Правильно! Наступний приклад."
                if self.score >= self.math_goal:
                    self.math_game_over = True
                    self.math_final_score = self.score
                    self.math_won = True
                    self.input_text = ""
                    return
                self.generate_math_question()
            else:
                self.message = "Неправильно. Подумай ще."

        elif self.active_game == "memory":
            if pygame.time.get_ticks() < self.show_word_until:
                self.message = "Спочатку дочекайся, поки слово зникне."
            elif answer.upper() == self.memory_word:
                self.score += 1
                self.message = "Правильно! Нове слово."
                self.start_memory_game()
            else:
                self.message = "Неправильно. Спробуй ще раз."

        self.input_text = ""

    def draw(self):
        if self.active_game is None:
            self.draw_menu()
        elif self.active_game == "math_difficulty":
            self.draw_difficulty_menu()
        else:
            self.draw_game()
