import os
import pygame
import sys

from scene_objects import SceneObjectManager
from settings import *
from pet import Pet
from world import World
from quiz import Quiz
from ui import UI
from background import BackgroundManager


PLAYER_TYPE_NAMES = {
    "school": "Школяр",
    "student": "Студент",
    "adult": "Дорослий",
    "programmer": "Програміст",
}


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.scene_objects = SceneObjectManager()
        self.ui = UI(self.screen)
        self.background = BackgroundManager()

        self.running = True
        self.state = "ai_disclaimer"
        self.disclaimer_start_time = pygame.time.get_ticks()
        self.ai_disclaimer_button = None

        self.pause = False

        self.menu_buttons = {}
        self.player_type_buttons = {}
        self.back_button = None
        self.lock_buttons = {}

        self.player_type = "school"
        self.pet_talk_until = 0

        self.transition_active = False
        self.transition_alpha = 0
        self.transition_target_location = None

        self.world_transition_active = False
        self.world_transition_alpha = 0
        self.world_transition_text = ""

        self.show_quest = False
        self.show_task = False
        self.show_card_found = False

        self.current_task = None
        self.task_marker = None
        self.task_card = None

        self.task_buttons = []
        self.quiz_buttons = []

        self.card_animation_start = 0
        self.card_show_duration = 1600

        self.typing_text = ""
        self.typing_index = 0
        self.typing_timer = 0

        self.location_completed_markers = {}
        self.completed_locations = set()

        self.big_test_mode = False
        self.big_test_from_menu = False
        self.big_test_questions = []
        self.big_test_index = 0
        self.big_test_score = 0
        self.big_test_total = 15
        self.big_test_need_percent = 60

        self.test_result = None
        self.test_result_button = None

        self.new_game()

    def new_game(self):
        self.pet = Pet("Бім")
        self.world = World()
        self.quiz = Quiz()
        self.quiz.set_player_type(self.player_type)

        self.show_quest = False
        self.show_task = False
        self.show_card_found = False

        self.current_task = None
        self.task_marker = None
        self.task_card = None

        self.task_buttons = []
        self.quiz_buttons = []

        self.location_completed_markers = {}
        self.completed_locations = set()

        self.energy = 5
        self.max_energy = 5

        self.message = "Натискай на маркери в локації та проходь питання."
        self.pet_hint = "Проходь маркери по черзі."

        self.set_typing_text(self.get_location_text())

    def set_typing_text(self, text):
        self.typing_text = text
        self.typing_index = 0
        self.typing_timer = pygame.time.get_ticks()

    def get_visible_story_text(self):
        now = pygame.time.get_ticks()

        if now - self.typing_timer > 18 and self.typing_index < len(self.typing_text):
            self.typing_index += 1
            self.typing_timer = now

        return self.typing_text[:self.typing_index]

    def make_pet_speak(self):
        self.pet_talk_until = pygame.time.get_ticks() + 1800

    def is_pet_speaking(self):
        return pygame.time.get_ticks() < self.pet_talk_until

    def get_location_text(self):
        texts = {
            "Будинок": "Перша локація. Тут потрібно пройти чотири маркери.",
            "Лісова стежка": "Лісова стежка приховує нові навчальні завдання.",
            "Старий міст": "Старий міст перевірить уважність та логіку.",
            "Печера": "У печері кожен маркер відкриває окреме випробування.",
            "Зал символів": "Давні символи приховують питання та підказки.",
            "Підземне озеро": "Тиха вода й кристали ведуть до наступного світу.",
            "Місто знань": "Місто знань перевіряє уважність і мислення.",
            "Бібліотека": "У бібліотеці знання заховані серед книг.",
            "Вежа мудрості": "Фінальна локація перед великим тестом.",
        }

        return texts.get(self.world.get_location(), "Досліджуй локацію.")

    def get_location_key(self):
        return self.world.get_location()

    def get_location_objects(self):
        return self.scene_objects.get_objects(self.world.get_location())

    def get_completed_marker_set(self):
        location = self.get_location_key()

        if location not in self.location_completed_markers:
            self.location_completed_markers[location] = set()

        return self.location_completed_markers[location]

    def get_location_progress(self):
        total = len(self.get_location_objects())
        done = len(self.get_completed_marker_set())
        return done, total

    def get_quest_text(self):
        done, total = self.get_location_progress()

        if done < total:
            return (
                "Натискай на маркери та відповідай на питання.",
                f"Прогрес локації: {done}/{total}",
            )

        return (
            "Локацію завершено.",
            "Починається перехід далі.",
        )

    def reset_windows(self):
        self.show_quest = False
        self.show_task = False

    def close_overlays(self):
        self.reset_windows()
        self.show_card_found = False

    def start_game_with_type(self, player_type):
        self.player_type = player_type
        self.new_game()
        self.state = "game"

    def start_big_test_with_type(self, player_type):
        self.player_type = player_type
        self.quiz.set_player_type(player_type)
        self.start_big_test(from_menu=True)

    def get_big_test_questions(self):
        if hasattr(self.quiz, "get_big_test"):
            return self.quiz.get_big_test(
                self.player_type,
                self.big_test_total
            )

        return []

    def start_big_test(self, from_menu=False):
        self.big_test_mode = True
        self.big_test_from_menu = from_menu
        self.test_result = None
        self.test_result_button = None

        self.big_test_questions = self.get_big_test_questions()
        self.big_test_index = 0
        self.big_test_score = 0

        if not self.big_test_questions:
            self.test_result = {
                "passed": False,
                "percent": 0,
                "title": "Тест недоступний",
                "text": "Немає питань для великого тесту. Перевір файл quiz.py.",
            }
            self.state = "test_result"
            return

        self.current_task = self.big_test_questions[0]

        self.state = "big_test"
        self.show_task = False
        self.show_quest = False
        self.show_card_found = False

        if from_menu:
            self.message = "Тренувальний тест розпочато."
        else:
            self.message = "Фінальний тест розпочато автоматично."

        self.pet_hint = "Потрібно набрати мінімум 60%."
        self.make_pet_speak()

    def complete_big_test_answer(self, answer):
        if not self.current_task:
            return

        if self.quiz.check_answer(self.current_task, answer):
            self.big_test_score += 1

        self.big_test_index += 1

        if self.big_test_index < len(self.big_test_questions):
            self.current_task = self.big_test_questions[self.big_test_index]
            return

        percent = int((self.big_test_score / len(self.big_test_questions)) * 100)

        self.big_test_mode = False
        self.current_task = None

        passed = percent >= self.big_test_need_percent

        if passed:
            self.test_result = {
                "passed": True,
                "percent": percent,
                "title": "Вітаю! Тест пройдено!",
                "text": f"Ти набрав {percent}% правильних відповідей. Це успішний результат.",
            }
        else:
            self.test_result = {
                "passed": False,
                "percent": percent,
                "title": "Тест не пройдено",
                "text": f"Ти набрав {percent}%. Потрібно мінімум 60%.",
            }

        self.state = "test_result"

    def load_big_test_background(self):
        paths = [
            "assets/backgrounds/big_test.jpg",
            "big_test.jpg",
        ]

        for path in paths:
            if os.path.exists(path):
                image = pygame.image.load(path).convert()
                return pygame.transform.smoothscale(image, (WIDTH, HEIGHT))

        return None

    def draw_test_result(self):
        if not hasattr(self, "big_test_bg"):
            self.big_test_bg = self.load_big_test_background()

        if self.big_test_bg:
            self.screen.blit(self.big_test_bg, (0, 0))
        else:
            self.screen.fill((10, 12, 20))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        self.screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(300, 170, 600, 330)
        self.ui.transparent_panel(
            panel_rect,
            (18, 22, 34, 235),
            WHITE,
            22
        )

        title_color = SUCCESS if self.test_result["passed"] else RED

        title_img = self.ui.big_font.render(
            self.test_result["title"],
            True,
            title_color
        )
        self.screen.blit(
            title_img,
            title_img.get_rect(center=(WIDTH // 2, 235))
        )

        self.ui.wrap_text(
            self.test_result["text"],
            370,
            300,
            460,
            3,
            WHITE,
            self.ui.font,
            32
        )

        if self.test_result["passed"]:
            button_text = "На головне меню"
        else:
            if self.big_test_from_menu:
                button_text = "На головне меню"
            else:
                button_text = "Спробувати гру спочатку"

        self.test_result_button = pygame.Rect(460, 410, 280, 50)
        self.ui.draw_button(self.test_result_button, button_text)

    def start_marker_question(self, clicked_object):
        completed = self.get_completed_marker_set()
        marker_id = clicked_object.get("mark", clicked_object["name"])

        if marker_id in completed:
            self.message = f"Маркер «{clicked_object['name']}» уже пройдено."
            self.pet_hint = "Обери інший маркер."
            self.make_pet_speak()
            return

        self.task_marker = clicked_object
        self.current_task = self.quiz.get_location_task(
            self.world.get_location(),
            self.world.current_world
        )

        if self.current_task is None:
            self.message = "Усі питання для цієї локації вже використані."
            self.pet_hint = "Обери інший маркер."
            self.make_pet_speak()
            return

        self.show_task = True
        self.show_quest = False
        self.show_card_found = False

        self.message = f"Маркер «{clicked_object['name']}» відкрив питання."
        self.pet_hint = "Дай правильну відповідь."
        self.make_pet_speak()

    def complete_marker_question(self, answer):
        if not self.current_task or not self.task_marker:
            return

        if self.quiz.check_answer(self.current_task, answer):
            marker_id = self.task_marker.get("mark", self.task_marker["name"])
            self.get_completed_marker_set().add(marker_id)

            self.message = "Правильно! Маркер пройдено."
            self.pet_hint = "Чудово, рухаємось далі."
            self.pet.add_xp(5)

            self.check_location_finished()
        else:
            self.message = "Неправильна відповідь. Спробуй ще раз."
            self.pet_hint = "Не здавайся."
            self.make_pet_speak()

        self.show_task = False
        self.current_task = None
        self.task_marker = None

    def check_location_finished(self):
        done, total = self.get_location_progress()

        if total > 0 and done >= total:
            self.completed_locations.add(self.world.get_location())

            card = self.world.get_visible_card()

            if card:
                card.find_hint()
                card.complete_task()
                xp = card.collect()

                if xp > 0:
                    self.pet.add_xp(xp)
                    self.task_card = card
                    self.show_card_found = True
                    self.card_animation_start = pygame.time.get_ticks()

            self.message = "Локацію завершено. Перехід далі..."
            self.pet_hint = "Відкривається наступна сцена."
            self.make_pet_speak()

            pygame.time.set_timer(pygame.USEREVENT + 1, 900, loops=1)

    def go_to_next_location_or_test(self):
        locations = self.world.get_locations()
        current_index = self.world.current_location_index

        if current_index < len(locations) - 1:
            next_location = locations[current_index + 1]
            self.begin_location_transition(next_location)
            return

        if not self.world.is_last_world():
            self.start_world_transition()
            return

        self.start_big_test(from_menu=False)

    def begin_location_transition(self, location):
        self.transition_active = True
        self.transition_alpha = 0
        self.transition_target_location = location

        self.reset_windows()
        self.show_card_found = False

    def update_transition(self):
        if not self.transition_active:
            return

        self.transition_alpha += 12

        if self.transition_alpha >= 255 and self.transition_target_location:
            locations = self.world.get_locations()
            self.world.current_location_index = locations.index(self.transition_target_location)
            self.transition_target_location = None

            self.message = f"Локація: {self.world.get_location()}."
            self.pet_hint = "Проходь маркери."
            self.set_typing_text(self.get_location_text())

        if self.transition_alpha >= 390:
            self.transition_alpha = 0
            self.transition_active = False

    def start_world_transition(self):
        self.world_transition_active = True
        self.world_transition_alpha = 0
        self.world_transition_text = "ВІДКРИВАЄТЬСЯ НОВИЙ СВІТ..."

        self.reset_windows()
        self.show_card_found = False

    def update_world_transition(self):
        if not self.world_transition_active:
            return

        self.world_transition_alpha += 5

        if self.world_transition_alpha == 150:
            moved = self.world.next_world()

            if moved:
                self.energy = self.max_energy
                self.pet.add_xp(20)
                self.message = "Новий світ відкрито."
                self.pet_hint = "Нова пригода починається."
                self.set_typing_text(self.get_location_text())

        if self.world_transition_alpha >= 320:
            self.world_transition_active = False
            self.world_transition_alpha = 0

    def draw_world_transition(self):
        if not self.world_transition_active:
            return

        alpha = min(255, self.world_transition_alpha)

        if self.world_transition_alpha > 180:
            alpha = max(0, 255 - (self.world_transition_alpha - 180) * 2)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(255, alpha)))
        self.screen.blit(overlay, (0, 0))

        if 40 < self.world_transition_alpha < 260:
            font = pygame.font.SysFont("arial", 46)
            text_img = font.render(self.world_transition_text, True, YELLOW)
            rect = text_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text_img, rect)

    def draw_transition(self):
        if not self.transition_active:
            return

        alpha = self.transition_alpha

        if alpha > 255:
            alpha = 255 - (self.transition_alpha - 255)

        alpha = max(0, min(255, alpha))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))

    def draw_card_animation(self):
        if not self.show_card_found or not self.task_card:
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.card_animation_start

        if elapsed > self.card_show_duration:
            self.show_card_found = False
            self.task_card = None
            return

        progress = min(1, elapsed / 350)
        scale = 0.75 + progress * 0.25

        self.ui.draw_card_found(self.task_card, scale)

    def handle_menu_click(self, key):
        if key == "inspect":
            done, total = self.get_location_progress()
            self.message = f"У цій локації потрібно пройти маркери: {done}/{total}."
            self.pet_hint = "Натискай на золоті маркери."
            self.make_pet_speak()

    def lock_game(self):
        self.state = "lock"
        self.pause = False
        self.reset_windows()

    def unlock_game(self):
        self.state = "game"

    def handle_lock_click(self, pos):
        for key, rect in self.lock_buttons.items():
            if rect.collidepoint(pos):
                if key == "continue":
                    self.unlock_game()
                elif key == "menu":
                    self.state = "menu"
                    self.pause = False
                elif key == "exit":
                    self.running = False
                return

    def restart_game_after_failed_test(self):
        self.world = World()
        self.quiz = Quiz()
        self.quiz.set_player_type(self.player_type)

        self.location_completed_markers = {}
        self.completed_locations = set()

        self.current_task = None
        self.task_marker = None
        self.task_card = None

        self.show_task = False
        self.show_card_found = False
        self.show_quest = False

        self.message = "Спробуй пройти гру ще раз."
        self.pet_hint = "Починаємо з першої локації."
        self.set_typing_text(self.get_location_text())

        self.state = "game"

    def handle_keydown(self, event):
        if event.key == pygame.K_l and self.state == "game":
            self.lock_game()
            return

        if event.key == pygame.K_ESCAPE:
            if self.state in ["select_type", "test_select_type", "rules", "about", "test_result"]:
                self.state = "menu"
                return

            if self.state == "lock":
                self.unlock_game()
                return

            if self.state == "game":
                if self.show_quest or self.show_task:
                    self.reset_windows()
                else:
                    self.pause = not self.pause

            if self.state == "big_test":
                self.state = "menu"

    def handle_mouse_click(self, pos):
        if self.state == "ai_disclaimer":
            elapsed = pygame.time.get_ticks() - self.disclaimer_start_time

            if elapsed > 2500:
                if self.ai_disclaimer_button and self.ai_disclaimer_button.collidepoint(pos):
                    self.state = "menu"
            return

        if self.state == "menu":
            for key, rect in self.menu_buttons.items():
                if rect.collidepoint(pos):
                    if key == "play":
                        self.state = "select_type"
                    elif key == "test":
                        self.state = "test_select_type"
                    elif key == "rules":
                        self.state = "rules"
                    elif key == "about":
                        self.state = "about"
                    elif key == "exit":
                        self.running = False
                    return

        elif self.state == "test_result":
            if self.test_result_button and self.test_result_button.collidepoint(pos):
                if self.test_result["passed"]:
                    self.state = "menu"
                else:
                    if self.big_test_from_menu:
                        self.state = "menu"
                    else:
                        self.restart_game_after_failed_test()
                return

        elif self.state == "select_type":
            for key, rect in self.player_type_buttons.items():
                if rect.collidepoint(pos):
                    self.start_game_with_type(key)
                    return

        elif self.state == "test_select_type":
            for key, rect in self.player_type_buttons.items():
                if rect.collidepoint(pos):
                    self.start_big_test_with_type(key)
                    return

        elif self.state == "lock":
            self.handle_lock_click(pos)

        elif self.state in ["rules", "about"]:
            if self.back_button and self.back_button.collidepoint(pos):
                self.state = "menu"
                return

        elif self.state == "big_test":
            for rect, answer in self.quiz_buttons:
                if rect.collidepoint(pos):
                    self.complete_big_test_answer(answer)
                    return

        elif self.state == "game":
            if self.pause or self.transition_active or self.world_transition_active:
                return

            for key, rect in self.menu_buttons.items():
                if rect.collidepoint(pos):
                    self.handle_menu_click(key)
                    return

            if self.show_task:
                for rect, answer in self.task_buttons:
                    if rect.collidepoint(pos):
                        self.complete_marker_question(answer)
                        return

            if not self.show_task and not self.show_quest:
                clicked_object = self.scene_objects.handle_click(
                    self.world.get_location(),
                    pos
                )

                if clicked_object:
                    self.start_marker_question(clicked_object)
                    return

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.USEREVENT + 1:
                self.go_to_next_location_or_test()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def update(self):
        if self.state == "game" and not self.pause:
            self.update_transition()
            self.update_world_transition()

    def draw_game(self):
        self.background.draw(
            self.screen,
            self.world.current_world,
            self.world.get_location()
        )

        self.scene_objects.draw(
            self.screen,
            self.world.get_location(),
            self.ui.small_font
        )

        self.ui.draw_top_panel(
            self.pet,
            self.world,
            self.energy,
            PLAYER_TYPE_NAMES.get(self.player_type, "Школяр")
        )

        if hasattr(self.ui, "draw_left_menu"):
            all_buttons = self.ui.draw_left_menu()
            self.menu_buttons = {
                key: rect for key, rect in all_buttons.items()
                if key in ["inspect"]
            }

        done, total = self.get_location_progress()

        self.ui.draw_novel_box(
            self.world.get_location(),
            self.get_location_text(),
            f"{self.get_visible_story_text()}  Прогрес: {done}/{total}"
        )

        self.draw_card_animation()

        if self.show_quest:
            quest_text, progress_text = self.get_quest_text()
            self.ui.draw_quest_window(quest_text, progress_text)

        if self.show_task and self.current_task:
            self.task_buttons = self.ui.draw_quiz(self.current_task)

        self.ui.draw_pet_helper(
            self.pet,
            self.pet_hint,
            self.is_pet_speaking()
        )

        if self.pause:
            self.ui.draw_pause()

        self.draw_transition()
        self.draw_world_transition()

    def draw_big_test(self):
        if not hasattr(self, "big_test_bg"):
            self.big_test_bg = self.load_big_test_background()

        if self.big_test_bg:
            self.screen.blit(self.big_test_bg, (0, 0))
        else:
            self.screen.fill((10, 12, 20))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 95))
        self.screen.blit(overlay, (0, 0))

        info = (
            f"Великий тест     "
            f"Питання {self.big_test_index + 1}/{len(self.big_test_questions)}     "
            f"Правильних: {self.big_test_score}     "
            f"Прохід: 60%"
        )

        info_img = self.ui.small_font.render(info, True, WHITE)
        self.screen.blit(info_img, info_img.get_rect(center=(WIDTH // 2, 70)))

        if self.current_task:
            self.quiz_buttons = self.ui.draw_quiz(self.current_task)

    def draw_ai_disclaimer(self):
        self.screen.fill((0, 0, 0))

        now = pygame.time.get_ticks()
        elapsed = now - self.disclaimer_start_time
        alpha = min(255, elapsed // 4)

        title_font = pygame.font.SysFont("arial", 28, bold=True)
        text_font = pygame.font.SysFont("arial", 20)

        title = title_font.render("ІНФОРМАЦІЙНЕ ПОВІДОМЛЕННЯ", True, (230, 205, 120))
        title.set_alpha(alpha)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 210)))

        lines = [
            "У проєкті використовуються графічні матеріали,",
            "створені або частково створені за допомогою",
            "технологій штучного інтелекту.",
            "",
            "Проєкт створено виключно з навчальною метою.",
        ]

        y = 275
        for line in lines:
            img = text_font.render(line, True, (230, 230, 230))
            img.set_alpha(alpha)
            self.screen.blit(img, img.get_rect(center=(WIDTH // 2, y)))
            y += 34

        if elapsed > 2500:
            self.ai_disclaimer_button = pygame.Rect(WIDTH // 2 - 115, 500, 230, 46)
            self.ui.draw_button(self.ai_disclaimer_button, "Продовжити")

    def draw(self):
        if self.state == "ai_disclaimer":
            self.draw_ai_disclaimer()

        elif self.state == "menu":
            self.menu_buttons = self.ui.draw_main_menu()

        elif self.state == "select_type":
            self.player_type_buttons = self.ui.draw_player_type_screen()

        elif self.state == "test_select_type":
            self.player_type_buttons = self.ui.draw_player_type_screen()

        elif self.state == "rules":
            self.back_button = self.ui.draw_rules_screen()

        elif self.state == "about":
            self.back_button = self.ui.draw_about_screen()

        elif self.state == "lock":
            self.lock_buttons = self.ui.draw_lock_screen()

        elif self.state == "game":
            self.draw_game()

        elif self.state == "big_test":
            self.draw_big_test()

        elif self.state == "test_result":
            self.draw_test_result()

        pygame.display.update()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()