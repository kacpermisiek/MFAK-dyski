import pygame
from disk import Disk
import settings
import thorpy

black = (0, 0, 0)


def main():
    screen = pygame.display.set_mode([settings.display_size_x, settings.display_size_y])
    pygame.init()
    pygame.display.flip()
    clock = pygame.time.Clock()
    disks = [Disk(screen) for i in range(settings.N)]

    slider1 = thorpy.SliderX(100, (1, 1000), "Number of disks", type_=int, initial_value=1000)
    slider1.set_font_color(black)
    slider2 = thorpy.SliderX(100, (0.5, 2), "size multiplier", type_=float, initial_value=1.0)
    slider2.set_font_color(black)
    box = thorpy.Box(elements=[slider1, slider2])
    menu = thorpy.Menu(box)

    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((10, 10))
    box.set_main_color((255, 255, 255, 100))

    running = True
    while running:
        dt = clock.tick(30) * .0001 * settings.FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    settings.animation = 1
                if event.key == pygame.K_2:
                    settings.animation = 2
                if event.key == pygame.K_3:
                    settings.animation = 3
                if event.key == pygame.K_4:
                    settings.animation = 4
                if event.key == pygame.K_5:
                    settings.animation = 5

        match settings.animation:
            case 1:
                # Animacja grawitacji
                for i in range(slider1.get_value()):
                    disks[i].gravity(dt, slider2.get_value())
            case 2:
                # Animacja przyciagania na pozycje kursora
                for i in range(slider1.get_value()):
                    disks[i].focus_on_cursor(dt, slider2.get_value())
            case 3:
                # Animacja przyciagania do srodka kursora
                for i in range(slider1.get_value()):
                    disks[i].center_force(dt, slider2.get_value())
            case 4:
                # Zatrzymanie animacji, zerowanie predkosci dyskow
                for i in range(slider1.get_value()):
                    disks[i].pause()
            case 5:
                for i in range(slider1.get_value()):
                    disks[i].new_force(dt, slider2.get_value())

        # Rysowanie dyskow
        for i in range(slider1.get_value()):
            disks[i].draw(slider2.get_value())

        pygame.display.flip()
        menu.react(event)
        box.blit()
        box.update()

        screen.blit(settings.background, (0, 0))
    pygame.quit()


if __name__ == '__main__':
    main()
