import os
import pygame
from settings import Settings

class ButtonHub():
    def __init__(self, settings: Settings):
        self.settings = settings
        self.button_quit_handlers = []
        self.pending_next, self.pending_back, self.pending_switch_to_primary, self.pending_switch_to_secondary = False, False, False, False

        self.button_quit_handlers.append(lambda: os._exit(0))

        if ButtonHub.is_rbpi():
            print("Device recognized as Raspbery PI")
            import RPi.GPIO as GPIO
            from interaction.gpio_button_handler import GpioButtonHandler
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.settings.gpio_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            cb = GpioButtonHandler(self.settings.gpio_button_pin, self.button_handler, bouncetime=150)
            cb.start()
            GPIO.add_event_detect(self.settings.gpio_button_pin, GPIO.RISING, callback=cb)

    @staticmethod
    def is_rbpi():
        return 'arm' in os.uname()[4] or 'aarch64' in os.uname()[4]

    def handle_keydown(self, key_code):
        if key_code == pygame.K_SPACE or key_code == pygame.K_RETURN: 
            self.trigger_short_press()
        elif key_code == pygame.K_RIGHT or key_code == pygame.HAT_RIGHT: 
            self.next_button_handler()
        elif key_code == pygame.K_LEFT or key_code == pygame.HAT_LEFT: 
            self.back_button_handler()
        elif key_code == pygame.K_ESCAPE or key_code == pygame.K_q:
            self.trigger_quit()

    def button_handler(self, duration):
        print("Physical button pressed with duration: " + str(duration) + " ms")

        if duration > self.settings.gpio_button_longpress_duration:
            self.back_button_handler()
        else:
            self.next_button_handler()

    def trigger_quit(self):
        print("Quit button pressed.")
        for handler in self.button_quit_handlers:
            handler()

    def back_button_handler(self):
        self.pending_back = True

    def next_button_handler(self):
        self.pending_next = True

    def switch_to_primary_handler(self):
        self.pending_switch_to_primary = True

    def switch_to_secondary_handler(self):
        self.pending_switch_to_secondary = True


    # TODO: extract to PendingButtonActions
    def back_flag_set(self):
        if self.pending_back:
            self.pending_back = False
            return True
        return False

    def next_flag_set(self):
        if self.pending_next:
            self.pending_next = False
            return True
        return False
    
    def switch_to_secondary_flag_set(self):
        if self.pending_switch_to_secondary:
            self.pending_switch_to_secondary = False
            return True
        return False
    
    def switch_to_primary_flag_set(self):
        if self.pending_switch_to_primary:
            self.pending_switch_to_primary = False
            return True
        return False
