import random
import pygame
from settings import *


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

        self.buttons = {}

    def draw_button(self, rect, text):
        mouse = pygame.mouse.get_pos()
        color = BUTTON_HOVER if rect.collidepoint(mouse) else BUTTON

        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, YELLOW, rect, 2, border_radius=12)

        img = self.font.render(text, True, WHITE)
        self.screen.blit(img, img.get_rect(center=rect.center))

    def draw_menu(self):
        self.screen.fill((12, 16, 28))

        title = self.big_font.render("Мініігри", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))

        subtitle = self.small_font.render(
            "Тут потрібно вводити відповіді вручну з клавіатури",
            True,
            TEXT_MUTED
        )
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 135)))

        self.buttons = {
            "number": pygame.Rect(WIDTH // 2 - 170, 210, 340, 55),
            "math": pygame.Rect(WIDTH // 2 - 170, 285, 340, 55),
            "memory": pygame.Rect(WIDTH // 2 - 170, 360, 340, 55),
            "back": pygame.Rect(WIDTH // 2 - 170, 470, 340, 55),
        }

        self.draw_button(self.buttons["number"], "Вгадай число")
        self.draw_button(self.buttons["math"], "Математичний спринт")
        self.draw_button(self.buttons["memory"], "Пам'ять")
        self.draw_button(self.buttons["back"], "Назад")

    def start_number_game(self):
        self.active_game = "number"
        self.target_number = random.randint(1, 20)
        self.input_text = ""
        self.message = "Я загадав число від 1 до 20. Введи відповідь."
        self.score = 0

    def start_math_game(self):
        self.active_game = "math"
        self.score = 0
        self.input_text = ""
        self.generate_math_question()

    def start_memory_game(self):
        self.active_game = "memory"
        self.input_text = ""
        words = ["КІТ", "ЛІС", "МІСТ", "КНИГА", "ПЕЧЕРА", "ЗІРКА", "КОМАНДА"]
        self.memory_word = random.choice(words)
        self.show_word_until = pygame.time.get_ticks() + 2500
        self.message = "Запам'ятай слово, потім введи його з клавіатури."

    def generate_math_question(self):
        a = random.randint(5, 30)
        b = random.randint(2, 20)
        op = random.choice(["+", "-", "*"])

        if op == "+":
            correct = a + b
        elif op == "-":
            correct = a - b
        else:
            correct = a * b

        self.current_question = {
            "text": f"{a} {op} {b} = ?",
            "answer": str(correct)
        }

        self.message = "Введи правильну відповідь."

    def draw_input_box(self):
        box = pygame.Rect(WIDTH // 2 - 180, 400, 360, 55)
        pygame.draw.rect(self.screen, (25, 30, 45), box, border_radius=10)
        pygame.draw.rect(self.screen, YELLOW, box, 2, border_radius=10)

        text = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(text, (box.x + 18, box.y + 14))

    def draw_game(self):
        self.screen.fill((12, 16, 28))

        title = self.big_font.render("Мінігра", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

        msg = self.font.render(self.message, True, WHITE)
        self.screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 145)))

        if self.active_game == "number":
            hint = self.font.render("Введи число та натисни Enter", True, TEXT_MUTED)
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 240)))

        elif self.active_game == "math":
            q = self.big_font.render(self.current_question["text"], True, WHITE)
            self.screen.blit(q, q.get_rect(center=(WIDTH // 2, 250)))

        elif self.active_game == "memory":
            now = pygame.time.get_ticks()

            if now < self.show_word_until:
                word = self.big_font.render(self.memory_word, True, YELLOW)
                self.screen.blit(word, word.get_rect(center=(WIDTH // 2, 250)))
            else:
                hint = self.font.render("Введи слово, яке було показано", True, TEXT_MUTED)
                self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 250)))

        self.draw_input_box()

        score_text = self.small_font.render(f"Рахунок: {self.score}", True, TEXT_MUTED)
        self.screen.blit(score_text, (30, 30))

        self.buttons = {
            "back": pygame.Rect(WIDTH // 2 - 120, 520, 240, 50)
        }

        self.draw_button(self.buttons["back"], "Назад")

    def handle_click(self, pos):
        if self.active_game is None:
            menu_buttons = {
                "number": pygame.Rect(WIDTH // 2 - 170, 210, 340, 55),
                "math": pygame.Rect(WIDTH // 2 - 170, 285, 340, 55),
                "memory": pygame.Rect(WIDTH // 2 - 170, 360, 340, 55),
                "back": pygame.Rect(WIDTH // 2 - 170, 470, 340, 55),
            }

            if menu_buttons["number"].collidepoint(pos):
                self.start_number_game()
                return None

            if menu_buttons["math"].collidepoint(pos):
                self.start_math_game()
                return None

            if menu_buttons["memory"].collidepoint(pos):
                self.start_memory_game()
                return None

            if menu_buttons["back"].collidepoint(pos):
                return "back"

            else:
                back_button = pygame.Rect(WIDTH // 2 - 120, 520, 240, 50)

                if back_button.collidepoint(pos):
                    self.active_game = None
                    self.input_text = ""
                    self.message = "Оберіть мінігру"
                    return None

            return None

        else:
            if self.buttons.get("back") and self.buttons["back"].collidepoint(pos):
                self.active_game = None
                self.input_text = ""
                self.message = "Оберіть мінігру"

        return None

    def handle_keydown(self, event):
        if self.active_game is None:
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
            if answer == self.current_question["answer"]:
                self.score += 1
                self.message = "Правильно! Наступний приклад."
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
        else:
            self.draw_game()