class Settings:
    def __init__(self):
		
        # Run in full screen
        self.fullscreen = True
        
        # dev mode
        self.dev_mode: bool = False

        # media folder
        # will be replaced by commandline param
        self.media_folder: str = "../samples"

        # duration in seconds
        self.duration: int = 10 * 60

     

        # Background
        # When both are enabled, they will be chosen by random
        self.background_patterns = True
        self.background_solid_color = True
        self.blur_background = True
        self.blur_background_radius = 6

        # Alpha value of the background - colors of the background will not be as strong as the colors of the photo
        # They will be projected against neutral gray that is controlled by background_lightness and where 0.5 means 50% gray
        self.background_alpha: float = 0.05
        self.background_lightness: float = 0.1

        # PPI (pixels per inch) of the background
        # Lower values will result in more repetitions of the background patterns
        self.background_ppi_min: int = 200
        self.background_ppi_max: int = 600
        self.background_amount_min: float = 0.3
        self.background_amount_max: float = 0.8

        # Border thicknesses and colors
        # Inner border is considered part of the picture and is always black
        # Inner border is also not displayed when image goes fullscreen
        # Outer border is only displayed on the sides where there is no real screen border
        # It's color should therefore match the color of the material around the screen
        self.outer_border_color = (231, 231, 223)
        self.inner_border_color = (231, 231, 223)
        self.border_inner: int = 0
        self.border_outer: int = 0

        

        # Whether to display date in top-left corner and caption in main content
        self.display_date: bool = True
        self.display_caption: bool = True

        # Physical button RPI
        self.gpio_button_pin = 23
        self.gpio_button_longpress_duration = 600

        # Prepared images buffer size - how many images are prepared in advance
        self.prepared_images_buffer_size = 10

        # Target line length for image comment
        # After target length comment will be broken into new line at the first space
        self.image_comment_target_line_length = 100
 
