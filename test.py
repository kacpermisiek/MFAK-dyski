import pygame
import math as m

a = pygame.math.Vector2(-10, 13)


print(m.sqrt(a.length()) ** 2)
print(a.length())
print(m.sqrt(a.x ** 2 + a.y ** 2))
