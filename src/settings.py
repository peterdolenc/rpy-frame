class Settings:

    def __init__(self):

        # duration in seconds
        self.duration = 20
 
        # This setting is basically inverted setting how much to zoom-in wide images
        #
        # If image is wider than the screen, then black bars on top and bottom will appear
        # Min controls the scenario when image is just slightly wider than the screen and by setting allowed amount to
        # non-zero you can avoid small black bars in these almost-fit images
        # Min 0.1 will zoom the image in slightly when image is only 10% wider than the screen
        # Max controls the images that are way wider than the screen and determines how much these will be
        # zoomed out (black bars) in desire to fit them on one screen.
        # Max 0.6 will allow only 40% of the screen to be taken by the image (wery thin/wide image)
        self.wide_edge_max = 0.1
        self.wide_edge_min = 0.05

        # This setting is basically inverted setting for how much to zoom-in portrait images
        #
        # If image is narrower than the screen, then black bars on left and right will appear
        # Min controls the scenario when image is just slightly higher than the screen and by
        # setting allowed amount to non-zero you can avoid small black bars in these almost-fit images
        # Min 0.1 will zoom the image in slightly when image is only 10% higher than the screen
        # Max controls the images that are way taller than the screen and determines how much these will be
        # zoomed out (black bars) in desire to fit them on one screen.
        # Max 0.6 will allow only 40% of the screen to be taken by the image (normal portrait image on 16:9 screen)
        self.portrait_edge_max = 0.1
        self.portrait_edge_min = 0.1


