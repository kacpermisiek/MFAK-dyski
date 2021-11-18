import pygame
import math as m
from random import uniform, randint
from colors import colors
import settings


class Disk:

    # Mnoznik tlumienia predkosci przy odbiciu
    damping = 0.6
    G = 6.67
    M = 10000

    def __init__(self, screen):
        self.screen = screen
        self.r = uniform(5, 10)
        #self.m = self.r * 0.08
        self.pos = pygame.math.Vector2((uniform(2 * self.r, settings.display_size_x - 2 * self.r)),
                                       (uniform(2 * self.r, settings.display_size_y - 2 * self.r)))
        self.V = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        self.F = pygame.math.Vector2(0, 0)
        self.a = pygame.math.Vector2(0, 0)
        self.color = colors[randint(0, len(colors) - 1)]

    def __str__(self):
        return f"x: {self.pos.x}, y: {self.pos.y} r: {self.r} color: {self.color}"

    def draw(self, size_multiplier):
        pygame.draw.circle(self.screen, self.color, (self.pos.x, self.pos.y), self.r * size_multiplier)

    # Sila grawitacji
    def gravity(self, dt, size_multiplier):
        self.pos += self.V * dt
        self.V.y += settings.g * dt
        self.air_resistance(dt, size_multiplier)
        self.check_bounds(size_multiplier)

    # Sila przyciagania w miejscu kursora
    def focus_on_cursor(self, dt, size_multiplier):
        self.F = (pygame.math.Vector2(pygame.mouse.get_pos()) - self.pos).normalize()
        self.V += self.F * dt * 0.5
        self.pos += self.V
        self.air_resistance(dt, size_multiplier)
        self.check_bounds(size_multiplier)

    # Opor aerodynamiczny
    def air_resistance(self, dt, size_multiplier):
        self.V += -6 * m.pi * self.V * 0.00001708 * self.r

    # Sila przyciagania w srodku ukladu
    def center_force(self, dt, size_multiplier):
        self.F = (pygame.math.Vector2(settings.display_size_x / 2, settings.display_size_y / 2) - self.pos).normalize()
        self.V += self.F
        self.pos += self.V * dt * 0.5
        self.air_resistance(dt, size_multiplier)
        self.check_bounds(size_multiplier)

    # Resetowanie predkosci dysku
    def pause(self):
        self.V = pygame.math.Vector2(0, 0)

    # Funkcja odbijania dyskow o krawedzie ekranu
    def check_bounds(self, size_multiplier):
        if self.pos.y - self.r * size_multiplier < 0:
            self.V.y *= -self.damping
            self.pos.y = 1.1 * self.r * size_multiplier
        elif self.pos.y + self.r * size_multiplier > settings.display_size_y:
            self.V.y *= -self.damping
            self.pos.y = settings.display_size_y - self.r * size_multiplier

        if self.pos.x - self.r < 0:
            self.V.x *= -self.damping
            self.pos.x = self.r * size_multiplier
        elif self.pos.x + self.r * size_multiplier > settings.display_size_x:
            self.V.x *= -self.damping
            self.pos.x = settings.display_size_x - 1.1 * self.r * size_multiplier

    def new_force(self, dt, size_multiplier):
        cx = settings.display_size_x / 2
        cy = settings.display_size_y / 2
        x = self.pos.x - cx
        y = self.pos.y - cy

        R = pygame.math.Vector2(x, y).length()
        if R > 50:
            ax = -((self.G * self.M * x) / (R ** 3))
            ay = -((self.G * self.M * y) / (R ** 3))

        else:
            ax, ay = 0.01, 0.01

        self.a = pygame.math.Vector2(ax, ay)
        self.V.x += (self.a.x * dt)
        self.V.y += (self.a.y * dt)

        self.pos += self.V

        self.air_resistance(dt, size_multiplier)
        self.check_bounds(size_multiplier)
