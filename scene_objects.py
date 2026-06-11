from cmath import rect

import pygame
from settings import *


class SceneObjectManager:
    def __init__(self):
        self.objects = {
            "Будинок": [
                {
                    "name": "Книжкова полиця",
                    "rect": pygame.Rect(105, 145, 160, 170),
                    "type": "task",
                    "mark": "1",
                    "marker_pos": (210, 180)
                },
                {
                    "name": "Стіл",
                    "rect": pygame.Rect(380, 300, 230, 135),
                    "type": "hint",
                    "mark": "2"
                },
                {
                    "name": "Вікно",
                    "rect": pygame.Rect(650, 80, 170, 250),
                    "type": "hint",
                    "mark": "3"
                },
                {
                    "name": "Скриня",
                    "rect": pygame.Rect(890, 350, 230, 120),
                    "type": "task",
                    "mark": "4"
                },
            ],

            "Лісова стежка": [
                {"name": "Старе дерево", "rect": pygame.Rect(210, 110, 160, 250), "type": "hint", "mark": "1"},
                {"name": "Камінь", "rect": pygame.Rect(560, 390, 150, 85), "type": "task", "mark": "2"},
                {"name": "Кущі", "rect": pygame.Rect(760, 330, 170, 110), "type": "task", "mark": "3"},
            ],

        "Старий міст": [
    {
        "name": "Дошка",
        "rect": pygame.Rect(95, 230, 160, 210),
        "type": "hint",
        "mark": "1",
        "marker_pos": (235, 350)
    },

    {
        "name": "Ліхтар",
        "rect": pygame.Rect(260, 45, 70, 330),
        "type": "task",
        "mark": "2",
        "marker_pos": (320, 300)
    },

    {
        "name": "Міст",
        "rect": pygame.Rect(430, 150, 420, 210),
        "type": "task",
        "mark": "3",
        "marker_pos": (640, 250)
    }
],
 "Печера": [
    {
        "name": "Кристал",
        "rect": pygame.Rect(95, 270, 260, 250),
        "type": "task",
        "mark": "1",
        "marker_pos": (270, 370)
    },

    {
        "name": "Каміння",
        "rect": pygame.Rect(720, 250, 350, 270),
        "type": "hint",
        "mark": "2",
        "marker_pos": (895, 375)
    },

    {
        "name": "Темний прохід",
        "rect": pygame.Rect(450, 120, 330, 300),
        "type": "task",
        "mark": "3",
        "marker_pos": (615, 285)
    },
],       
"Зал символів": [
    {
        "name": "Руни",
        "rect": pygame.Rect(90, 80, 220, 300),
        "type": "task",
        "mark": "1",
        "marker_pos": (200,220)
    },

    {
        "name": "Кам'яна плита",
        "rect": pygame.Rect(350, 390, 520, 180),
        "type": "hint",
        "mark": "2",
        "marker_pos": (600, 520)
    },

    {
        "name": "Магічне світло",
        "rect": pygame.Rect(830, 120, 220, 240),
        "type": "task",
        "mark": "3",
        "marker_pos": (980, 290)
    },
],
"Підземне озеро": [
    {
        "name": "Берег",
        "rect": pygame.Rect(220, 420, 180, 100),
        "type": "hint",
        "mark": "1",
        "marker_pos": (260, 500)
    },

    {
        "name": "Вода",
        "rect": pygame.Rect(520, 420, 260, 110),
        "type": "task",
        "mark": "2",
        "marker_pos": (600, 490)
    },

    {
        "name": "Кристал",
        "rect": pygame.Rect(930, 280, 140, 180),
        "type": "task",
        "mark": "3",
        "marker_pos": (1070, 410)
    },
],
            "Місто знань": [
                {"name": "Двері", "rect": pygame.Rect(210, 320, 110, 150), "type": "task", "mark": "1"},
                {"name": "Вивіска", "rect": pygame.Rect(515, 220, 170, 85), "type": "hint", "mark": "2"},
                {"name": "Фонтан", "rect": pygame.Rect(860, 460, 150, 110), "type": "task", "mark": "3"},
            ],

            "Бібліотека": [
                {"name": "Полиця", "rect": pygame.Rect(290, 180, 150, 290), "type": "task", "mark": "1"},
                {"name": "Старий том", "rect": pygame.Rect(870, 240, 130, 130), "type": "task", "mark": "2"},
                {"name": "Стіл", "rect": pygame.Rect(530, 470, 190, 85), "type": "hint", "mark": "3"},
            ],

            "Вежа мудрості": [
                {"name": "Портал", "rect": pygame.Rect(550, 180, 180, 190), "type": "task", "mark": "1"},
                {"name": "Руни", "rect": pygame.Rect(330, 275, 130, 115), "type": "hint", "mark": "2"},
                {"name": "Кристал", "rect": pygame.Rect(890, 275, 115, 115), "type": "task", "mark": "3"},
            ],
        }

    def get_objects(self, location):
        return self.objects.get(location, [])

    def draw_marker(self, screen, obj, font, small_font):
        rect = obj["rect"]
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)

        if "marker_pos" in obj:
            center_x, center_y = obj["marker_pos"]
        else:
            center_x = rect.centerx
            center_y = rect.centery

        radius = 18 if hover else 14
        glow_radius = 28 if hover else 20
        glow_alpha = 95 if hover else 45

        glow = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (255, 214, 90, glow_alpha),
            (glow_radius, glow_radius),
            glow_radius
        )

        screen.blit(
            glow,
            (center_x - glow_radius, center_y - glow_radius)
        )

        pygame.draw.circle(
            screen,
            (20, 24, 35),
            (center_x, center_y),
            radius
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (center_x, center_y),
            radius,
            2
        )

        mark_img = font.render(obj["mark"], True, YELLOW)
        mark_rect = mark_img.get_rect(center=(center_x, center_y))
        screen.blit(mark_img, mark_rect)

        if hover:
            label_img = small_font.render(obj["name"], True, WHITE)

            label_w = label_img.get_width() + 28
            label_h = 34

            label_x = center_x - label_w // 2
            label_y = center_y - 64

            label_panel = pygame.Surface((label_w, label_h), pygame.SRCALPHA)

            pygame.draw.rect(
                label_panel,
                (20, 24, 35, 235),
                label_panel.get_rect(),
                border_radius=10
            )

            pygame.draw.rect(
                label_panel,
                YELLOW,
                label_panel.get_rect(),
                1,
                border_radius=10
            )

            screen.blit(label_panel, (label_x, label_y))
            screen.blit(label_img, (label_x + 14, label_y + 8))

    def draw(self, screen, location, font):
        small_font = pygame.font.SysFont("arial", 17)

        for obj in self.get_objects(location):
            self.draw_marker(screen, obj, font, small_font)

    def handle_click(self, location, pos):
        for obj in self.get_objects(location):
            if obj["rect"].collidepoint(pos):
                return obj

        return None