import pygame


class Gui:

    def __init__(self):
        pygame.init()
        self.mode = max(pygame.display.list_modes())
        # for testing on macbook
        self.mode = (1440, 900)
        pygame.display.set_caption('rpy slideshow')
        pygame.display.set_mode(self.mode, pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.get_surface()
        self.screen.fill((0, 0, 0))

    def get_screen_resolution(self):
        return self.mode

    def display_image(self, image, posx=0, posy=0):
        self.screen.fill((0, 0, 0))
        self.screen.blit(image, (posx, posy))
        pygame.display.update()
        pygame.event.pump()



