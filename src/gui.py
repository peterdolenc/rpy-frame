import pygame


class Gui:

    def __init__(self):
        pygame.init()
        self.mode = [1280, 720]
        pygame.display.set_mode(self.mode, pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.screen = pygame.display.get_surface()
        self.screen.fill((0, 0, 0))

    def get_screen_resolution(self):
        return self.mode

    def display_image(self, image, posx = 0, posy = 0):
        self.screen.fill((0, 0, 0))
        self.screen.blit(image, (posx, posy))
        pygame.display.update()
        pygame.event.pump()



