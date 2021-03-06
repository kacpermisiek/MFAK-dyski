import pygame
import math as m
from random import uniform, randint
from colors import colors
import settings


class Disk:

    # Multiplier of damping after hit at bounds
    damping = 0.6

    # Physic variables
    G = 6.67
    M = 10000

    def __init__(self, screen):
        self.screen = screen
        self.r = uniform(5, 10)
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

    # Gravity force
    def gravity(self, dt, size_multiplier):
        self.pos += self.V * dt
        self.V.y += settings.g * dt

    # Animation of center on mouse position
    def focus_on_cursor(self, dt, size_multiplier):
        cx = pygame.mouse.get_pos()[0]
        cy = pygame.mouse.get_pos()[1]
        self.center_force(dt, size_multiplier, cx, cy)

    # Animation of center force
    def focus_on_center(self, dt, size_multiplier):
        cx = settings.display_size_x / 2
        cy = settings.display_size_y / 2
        self.center_force(dt, size_multiplier, cx, cy)

    # Air resistance
    def air_resistance(self):
        self.V += -6 * m.pi * self.V * 0.00001708 * self.r

    # Reset velocity of disk
    def pause(self):
        self.V = pygame.math.Vector2(0, 0)

    # Check if position of disk is near to bounds, if yes - revert velocity
    def check_bounds(self, size_multiplier):
        if self.pos.y - self.r * size_multiplier < 0:
            self.V.y *= -self.damping
            self.pos.y = self.r * size_multiplier
            self.pos.y = self.r * size_multiplier
        elif self.pos.y + self.r * size_multiplier > settings.display_size_y:
            self.V.y *= -self.damping
            self.pos.y = settings.display_size_y - self.r * size_multiplier

        if self.pos.x - self.r < 0:
            self.V.x *= -self.damping
            self.pos.x = self.r * size_multiplier
        elif self.pos.x + self.r * size_multiplier > settings.display_size_x:
            self.V.x *= -self.damping
            self.pos.x = settings.display_size_x - 1.1 * self.r * size_multiplier

    # Function that is calculating acceleration from gravity
    def center_force(self, dt, size_multiplier, cx, cy):
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
