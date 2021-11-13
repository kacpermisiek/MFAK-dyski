import pygame
import math as m
from random import uniform, randint
from colors import colors
import settings


class Disk:
    def __init__(self, screen):
        self.r = uniform(5, 10)
        self.x = uniform(0 + 2 * self.r, settings.display_size_x - 2 * self.r)
        self.y = uniform(0 + 2 * self.r, settings.display_size_y - 2 * self.r)
        self.color = colors[randint(0, len(colors) - 1)]
        self.screen = screen
        self.Vx = 100
        self.Vy = 0
        self.Fx = 0
        self.Fy = 0

    def __str__(self):
        return f"x: {self.x}, y: {self.y} r: {self.r} color: {self.color}"

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def gravity(self, dt):
        self.x += self.Vx * dt
        self.y += self.Vy * dt

        self.Vy += settings.g * dt
        self.check_bounds()

    def center_force(self, dt):
        self.x += self.Vx * dt
        self.y += self.Vy * dt

        cx = settings.display_size_x / 2
        cy = settings.display_size_y / 2
        self.Fx = cx - self.x
        self.Fy = cy - self.y

        self.Vx += self.Fx * dt * 0.1
        self.Vy += self.Fy * dt * 0.1
        self.check_bounds()

    def check_bounds(self):
        if self.y - self.r < 0:
            self.Vy *= -1
            self.y += self.r
        elif self.y + self.r > settings.display_size_y:
            self.Vy *= -1
            self.y -= self.r

        if self.x - self.r < 0:
            self.Vx *= -1
            self.x += self.r
        elif self.x + self.r > settings.display_size_x:
            self.Vx *= -1
            self.x -= self.r

