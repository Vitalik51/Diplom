import os
import pygame
from settings import *


BACKGROUND_IMAGES = {
    "Будинок": "house.jpg",
    "Лісова стежка": "forest.jpg",
    "Старий міст": "bridge.jpg",

    "Печера": "cave.jpg",
    "Зал символів": "symbols.jpg",
    "Підземне озеро": "lake.jpg",

    "Місто знань": "city.jpg",
    "Бібліотека": "library.jpg",
    "Вежа мудрості":"tower.jpg",
}


class BackgroundManager:
    def __init__(self):
        self.loaded_images = {}

    def load_image(self, path):
        if not path:
            return None

        if path in self.loaded_images:
            return self.loaded_images[path]

        if os.path.exists(path):
            image = pygame.image.load(path).convert()
            image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
            self.loaded_images[path] = image
            return image

        return None

    def draw_fallback_background(self, screen, world):
        if world == 1:
            top = (70, 120, 170)
            bottom = (35, 60, 85)
        elif world == 2:
            top = (45, 40, 80)
            bottom = (25, 22, 45)
        else:
            top = (80, 65, 120)
            bottom = (30, 25, 60)

        for y in range(HEIGHT):
            ratio = y / HEIGHT

            r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
            g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
            b = int(top[2] * (1 - ratio) + bottom[2] * ratio)

            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        font = pygame.font.SysFont("arial", 34)
        small_font = pygame.font.SysFont("arial", 20)

        title = font.render("ФОН НЕ ЗНАЙДЕНО", True, (255, 215, 90))
        hint = small_font.render(
            "Поклади картинку в assets/backgrounds/ і вкажи шлях у background.py",
            True,
            (230, 230, 230)
        )

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

    def draw_dark_overlay(self, screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 75))
        screen.blit(overlay, (0, 0))

    def draw_vignette(self, screen):
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for i in range(160):
            alpha = int(i * 0.7)
            pygame.draw.rect(
                vignette,
                (0, 0, 0, alpha),
                (i, i, WIDTH - i * 2, HEIGHT - i * 2),
                2
            )

        screen.blit(vignette, (0, 0))

    def draw(self, screen, world, location):
        image_path = BACKGROUND_IMAGES.get(location)
        image = self.load_image(image_path)

        if image:
            screen.blit(image, (0, 0))
        else:
            self.draw_fallback_background(screen, world)

        self.draw_dark_overlay(screen)
        self.draw_vignette(screen)