import pygame


class Gui:

    def __init__(self):
        pygame.init()
        self.mode = [800, 600]
        pygame.display.set_mode(self.mode, pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.screen = pygame.display.get_surface()
        self.screen.fill((0, 0, 0))


    def display_image(self, image):
        resized_image = pygame.transform.smoothscale(image, self.mode)
        self.screen.blit(resized_image, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        pygame.event.pump()



