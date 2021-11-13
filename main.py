import pygame
from disk import Disk
import settings


def main():

    screen = pygame.display.set_mode([settings.display_size_x, settings.display_size_y])
    clock = pygame.time.Clock()
    disks = [Disk(screen) for _ in range(settings.N)]
    # disks = [Disk(screen)]
    # disks[0].r = 30

    running = True
    while running:
        dt = clock.tick(30) * .0001 * settings.FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        for disk in disks:
            #disk.gravity(dt)
            disk.center_force(dt)
            disk.draw()

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    main()
