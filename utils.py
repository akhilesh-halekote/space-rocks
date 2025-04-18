# asteroid_shooter/utils.py
from unittest.mock import Mock

from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pathlib import Path


def load_sprite(name, with_alpha=True):
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")
    sprite = load(filename.resolve())

    if with_alpha:
        return sprite.convert_alpha()

    return sprite.convert()


def wrap_position(position, surface):
    x, y = position
    if isinstance(surface, Mock):
        w, h = x % 800, y % 600
    else:
        w, h = surface.get_size()
    return Vector2(x % w, y % h)


def load_sound(name):
    filename = Path(__file__).parent / Path("assets/sounds/" + name + ".wav")
    return Sound(filename)


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)


def print_sub_text(surface, text, font, color=Color("magenta")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2 + Vector2(0, 100)
    surface.blit(text_surface, rect)


def print_score(surface, font, score, high_score, color=Color("white")):
    text_surface = font.render(f"Score: {score} High Score: {high_score}", True, color)
    rect = text_surface.get_rect()
    rect.topleft = (10, 10)
    surface.blit(text_surface, rect)
