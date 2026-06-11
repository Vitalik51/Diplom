import os
import pygame
from settings import *


PET_AVATAR = "pet1.png"


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.used_task_indexes = set()
        self.used_location_indexes = {}
        self.used_big_test_indexes = set()
        self.font = pygame.font.SysFont("arial", 23)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.tiny_font = pygame.font.SysFont("arial", 15)
        self.big_font = pygame.font.SysFont("arial", 36)
        self.title_font = pygame.font.SysFont("arial", 30)
        self.logo_font = pygame.font.SysFont("arial", 58)

        self.pet_avatar = self.load_avatar(PET_AVATAR)

    def load_avatar(self, path):
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(image, (88, 88))
        return None

    def draw_custom_menu_bg(self):
        if not hasattr(self, "menu_bg"):
            self.menu_bg = pygame.image.load("menu.jpg").convert()
            self.menu_bg = pygame.transform.smoothscale(self.menu_bg, (WIDTH, HEIGHT))

        self.screen.blit(self.menu_bg, (0, 0))

    def text(self, text, x, y, color=WHITE, font=None):
        font = font or self.font
        img = font.render(str(text), True, color)
        self.screen.blit(img, (x, y))

    def wrap_text(self, text, x, y, max_width, max_lines=3, color=WHITE, font=None, line_height=25):
        font = font or self.small_font
        words = str(text).split()
        lines = []
        line = ""

        for word in words:
            test = line + word + " "
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line.strip())
                line = word + " "

        if line:
            lines.append(line.strip())

        for i, line in enumerate(lines[:max_lines]):
            img = font.render(line, True, color)
            self.screen.blit(img, (x, y + i * line_height))

    def transparent_panel(self, rect, color=(20, 24, 35, 180), border_color=None, radius=18):
        surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=radius)

        if border_color:
            pygame.draw.rect(surface, border_color, surface.get_rect(), 1, border_radius=radius)

        self.screen.blit(surface, (rect[0], rect[1]))

    def draw_button(self, rect, label):
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)

        if hover:
            color = (55, 66, 100, 235)
            border = (230, 205, 110)
            text_color = YELLOW
        else:
            color = (25, 31, 48, 210)
            border = (90, 100, 145)
            text_color = WHITE

        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=16)
        pygame.draw.rect(surface, border, surface.get_rect(), 2 if hover else 1, border_radius=16)

        self.screen.blit(surface, rect.topleft)

        img = self.small_font.render(label, True, text_color)
        self.screen.blit(img, img.get_rect(center=rect.center))

    def draw_big_test_screen(self, question_data, current, total, score=0):
        self.screen.fill((12, 16, 28))

        self.transparent_panel(
            (180, 60, 840, 600),
            (18, 22, 36, 245),
            (90, 100, 145),
            24
        )

        title = f"Великий тест"
        self.text(title, 480, 95, YELLOW, self.big_font)

        info = f"Питання {current}/{total}   Правильних: {score}"
        self.text(info, 450, 145, TEXT_MUTED, self.small_font)

        self.wrap_text(
            question_data["question"],
            260,
            215,
            680,
            3,
            WHITE,
            self.font,
            32
        )

        buttons = []
        y = 335

        for answer in question_data["answers"]:
            rect = pygame.Rect(330, y, 540, 54)
            self.draw_button(rect, answer)
            buttons.append((rect, answer))
            y += 78

        return buttons
    
    def draw_main_menu(self):
        self.draw_custom_menu_bg()

        buttons = {}

        data = [
            ("play", "Грати"),
            ("test", "Тест"),
            ("rules", "Правила гри"),
            ("about", "Про гру"),
            ("exit", "Вийти"),
        ]

        button_width = 220
        button_height = 42
        x = WIDTH // 2 - button_width // 2 - 35
        y = 330 
        for key, label in data:
            rect = pygame.Rect(x, y, button_width, button_height)
            self.draw_button(rect, label)
            buttons[key] = rect
            y += 54

        return buttons

    def draw_player_type_screen(self):
        self.draw_custom_menu_bg()

        self.transparent_panel((250, 70, 700, 560), (15, 20, 35, 155), (95, 105, 145), 24)

        self.text("Хто ти?", 515, 105, YELLOW, self.logo_font)
        self.text("Обери профіль — питання будуть під твій рівень.", 390, 175, WHITE, self.small_font)

        buttons = {}

        variants = [
            ("school", "Школяр", "Легкі шкільні питання."),
            ("student", "Студент", "Логіка, навчання, аналіз, джерела."),
            ("adult", "Дорослий", "Бізнес, економіка, фінанси."),
            ("programmer", "Програміст", "Python, алгоритми, код і логіка."),
        ]

        y = 240

        for key, title, desc in variants:
            rect = pygame.Rect(350, y, 500, 68)

            mouse = pygame.mouse.get_pos()
            hover = rect.collidepoint(mouse)

            color = (38, 44, 62, 220) if hover else (25, 31, 48, 200)

            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(surface, color, surface.get_rect(), border_radius=18)
            pygame.draw.rect(surface, (95, 105, 145), surface.get_rect(), 1, border_radius=18)
            self.screen.blit(surface, rect.topleft)

            self.text(title, rect.x + 25, rect.y + 12, YELLOW, self.font)
            self.wrap_text(desc, rect.x + 25, rect.y + 40, 450, 1, TEXT_MUTED, self.small_font, 20)

            buttons[key] = rect
            y += 86

        return buttons

    def draw_rules_screen(self):
        self.draw_custom_menu_bg()

        self.transparent_panel((190, 70, 820, 570), (15, 20, 35, 170), (95, 105, 145), 24)

        self.text("Правила гри", 475, 105, YELLOW, self.big_font)

        rules = [
            "1. Гравець проходить локації послідовно.",
            "2. У кожній локації потрібно натискати на золоті маркери.",
            "3. Кожен маркер відкриває окреме навчальне питання.",
            "4. Після проходження всіх маркерів локація автоматично змінюється.",
            "5. Після останньої локації запускається фінальний тест.",
            "6. Для проходження великого тесту потрібно набрати мінімум 60% правильних відповідей.",
        ]

        y = 175

        for rule in rules:
            self.wrap_text(rule, 250, y, 700, 2, WHITE, self.font, 28)
            y += 66

        back_rect = pygame.Rect(485, 565, 230, 42)
        self.draw_button(back_rect, "Назад")

        return back_rect

    def draw_about_screen(self):
        self.draw_custom_menu_bg()

        self.transparent_panel((210, 105, 780, 480), (15, 20, 35, 170), (95, 105, 145), 24)

        self.text("Про гру", 520, 145, YELLOW, self.big_font)

        text = (
            "Pet Worlds — це навчальна гра у форматі візуальної новели з елементами RPG. "
            "Гравець подорожує між локаціями, натискає на інтерактивні маркери, "
            "відповідає на питання, збирає картки-команди та проходить фінальний тест."
        )

        self.wrap_text(text, 280, 220, 650, 6, WHITE, self.font, 32)

        self.text("Особливості:", 280, 420, YELLOW, self.font)
        self.text("локації, маркери, питання, XP, питомeць Бім, фінальний тест.", 280, 455, TEXT_MUTED, self.small_font)

        back_rect = pygame.Rect(485, 515, 230, 42)
        self.draw_button(back_rect, "Назад")

        return back_rect

    def draw_lock_screen(self):
        self.screen.fill((14, 18, 30))
        self.transparent_panel((330, 110, 540, 470), (22, 26, 39, 220), (95, 105, 145), 22)

        self.text("ГРУ ЗАБЛОКОВАНО", 440, 295, YELLOW, self.big_font)
        self.text("Прогрес збережено у поточній сесії", 442, 345, TEXT_MUTED, self.small_font)

        buttons = {}

        data = [
            ("continue", "Продовжити", 395),
            ("menu", "Головне меню", 460),
            ("exit", "Вийти", 525),
        ]

        for key, label, y in data:
            rect = pygame.Rect(455, y, 290, 46)
            self.draw_button(rect, label)
            buttons[key] = rect

        return buttons

    def draw_top_panel(self, pet, world, energy, player_type_name):
        info = pet.get_info()

        self.transparent_panel((22, 15, WIDTH - 44, 68), (21, 25, 38, 210), None, 18)

        self.text("Pet Worlds", 45, 34, YELLOW, self.title_font)
        self.text(f"Світ: {world.get_name()}", 245, 40, WHITE, self.small_font)
        self.text(f"Локація: {world.get_location()}", 450, 40, TEXT_MUTED, self.small_font)
        self.text(f"Тип: {player_type_name}", 710, 40, WHITE, self.small_font)
        self.text(f"{info['name']} LVL {info['level']}", 855, 40, WHITE, self.small_font)
        self.text(f"XP {info['xp']}/{info['need_xp']}", 985, 40, YELLOW, self.small_font)

    def draw_left_menu(self):
        buttons = {}

        items = [
            ("inspect", "Підказка"),
        ]

        x = 28
        y = 125

        for key, label in items:
            rect = pygame.Rect(x, y, 125, 42)
            self.draw_button(rect, label)
            buttons[key] = rect
            y += 54

        return buttons
    
    def draw_pet_helper(self, pet, hint, speaking=False):
        x = WIDTH - 350
        y = 105

        self.transparent_panel((x, y, 315, 120), (22, 26, 39, 210), (95, 105, 145), 18)

        avatar_x = x + 18
        avatar_y = y + 16

        if self.pet_avatar:
            self.screen.blit(self.pet_avatar, (avatar_x, avatar_y))
        else:
            pygame.draw.circle(self.screen, SOFT_ORANGE, (avatar_x + 45, avatar_y + 45), 38)
            pygame.draw.circle(self.screen, BLACK, (avatar_x + 32, avatar_y + 38), 4)
            pygame.draw.circle(self.screen, BLACK, (avatar_x + 58, avatar_y + 38), 4)

        if speaking:
            pygame.draw.ellipse(self.screen, BLACK, (avatar_x + 39, avatar_y + 62, 18, 10))

        self.text(pet.name, x + 125, y + 23, YELLOW, self.small_font)

        self.wrap_text(
            hint,
            x + 125,
            y + 55,
            165,
            2,
            WHITE,
            self.small_font,
            22
        )

    def draw_novel_box(self, location, description, visible_text=None):
        shown_text = visible_text if visible_text is not None else description

        self.transparent_panel(
            (185, 585, WIDTH - 370, 105),
            (15, 18, 28, 210),
            WHITE,
            18
        )

        self.text(location, 215, 605, YELLOW, self.font)

        self.wrap_text(
            shown_text,
            215,
            640,
            WIDTH - 440,
            3,
            WHITE,
            self.small_font,
            24
        )

    def draw_card_found(self, card, scale=1.0):
        base_w = int(360 * scale)
        base_h = int(220 * scale)

        x = WIDTH // 2 - base_w // 2
        y = 145

        pygame.draw.rect(self.screen, CARD_BG, (x, y, base_w, base_h), border_radius=18)
        pygame.draw.rect(self.screen, DARK, (x, y, base_w, base_h), 2, border_radius=18)

        self.text("ЗНАЙДЕНО КАРТКУ", x + int(75 * scale), y + int(28 * scale), BLACK, self.small_font)
        self.text(card.name.upper(), x + int(120 * scale), y + int(75 * scale), BLACK, self.title_font)
        self.wrap_text(card.description, x + int(40 * scale), y + int(120 * scale), int(280 * scale), 2, BLACK, self.small_font, 22)
        self.text(f"+{card.xp_reward} XP", x + int(135 * scale), y + int(170 * scale), SOFT_PURPLE, self.font)

    def draw_quest_window(self, quest_text, progress_text):
        self.transparent_panel((280, 150, 640, 270), (18, 22, 34, 225), WHITE, 18)

        self.text("Поточне завдання", 455, 185, YELLOW, self.big_font)
        self.wrap_text(quest_text, 330, 250, 540, 3, WHITE, self.font, 30)
        self.text(progress_text, 420, 345, SUCCESS, self.font)

    def draw_quiz(self, question_data):
        self.transparent_panel((260, 125, 680, 470), (18, 22, 34, 235), WHITE, 18)

        self.text("Навчальне питання", 435, 160, YELLOW, self.big_font)
        self.wrap_text(question_data["question"], 320, 230, 560, 2, WHITE, self.font, 30)

        buttons = []
        y = 330

        for answer in question_data["answers"]:
            rect = pygame.Rect(390, y, 420, 52)
            self.draw_button(rect, answer)
            buttons.append((rect, answer))
            y += 70

        return buttons

    def draw_pause(self):
        self.transparent_panel((390, 210, 420, 260), (18, 22, 34, 225), WHITE, 18)

        self.text("Пауза", 530, 250, YELLOW, self.big_font)
        self.text("ESC - продовжити", 455, 335, WHITE, self.font)
        self.text("L - екран блокування", 455, 370, TEXT_MUTED, self.small_font)