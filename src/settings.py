class Settings:

    def __init__(self):

        # dev mode
        self.dev_mode: bool = False

        # media folder
        # will be replaced by commandline param
        self.media_folder: str = "../samples"

        # duration in seconds
        self.duration: int = 600
 
        # This setting is basically inverted setting how much to zoom-in wide images
        #
        # If image is wider than the screen, then black bars on top and bottom will appear
        # Min controls the scenario when image is just slightly wider than the screen and by setting allowed amount to
        # non-zero you can avoid small black bars in these almost-fit images
        # Min 0.1 will zoom the image in slightly when image is only 10% wider than the screen
        # Max controls the images that are way wider than the screen and determines how much these will be
        # zoomed out (black bars) in desire to fit them on one screen.
        # Max 0.6 will allow only 40% of the screen to be taken by the image (very thin/wide image)
        self.wide_edge_max: float = 0.2
        self.wide_edge_min: float = 0.1

        # This setting is basically inverted setting for how much to zoom-in portrait images
        #
        # If image is narrower than the screen, then black bars on left and right will appear
        # Min controls the scenario when image is just slightly higher than the screen and by
        # setting allowed amount to non-zero you can avoid small black bars in these almost-fit images
        # Min 0.1 will zoom the image in slightly when image is only 10% higher than the screen
        # Max controls the images that are way taller than the screen and determines how much these will be
        # zoomed out (black bars) in desire to fit them on one screen.
        # Max 0.6 will allow only 40% of the screen to be taken by the image (normal portrait image on 16:9 screen)
        self.portrait_edge_max: float = 0.5
        self.portrait_edge_min: float = 0.05

        # Alpha value of the background - colors of the background will not be as strong as the colors of the photo
        # They will be projected against neutral gray that is controlled by background_lightness and where 0.5 means 50% gray
        self.background_alpha: float = 0.15
        self.background_lightness: float = 0.0

        # PPI (pixels per inch) of the background
        # Lower values will result in more repetitions of the background patterns
        self.background_ppi: int = 400
        self.background_amount_min: float = 0.2
        self.background_amount_max: float = 0.6

        # Border thicknesses and colors
        # Inner border is considered part of the picture and is always black
        # Inner border is also not displayed when image goes fullscreen
        # Outer border is only displayed on the sides where there is no real screen border
        # It's color should therefore match the color of the material around the screen
        self.outer_border_color = (231, 231, 223)
        self.inner_border_color = (231, 231, 223)
        self.border_inner: int = 6
        self.border_outer: int = 6

        # Blur background
        self.blur_background = True
        self.blur_background_radius = 5

        # Whether to display date in top-left corner
        self.display_date: bool = False

        # Physical button RPI
        self.physical_button_pin = 23
        self.physical_button_longpress_duration = 1000



