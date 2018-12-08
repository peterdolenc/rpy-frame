import os
import time

from io_thread.thread_context import ThreadContext


class IoMain():
    def __init__(self, thread_context: ThreadContext):
        self.thread_context = thread_context
        self.settings = thread_context.settings

    def start(self):
        if IoMain.is_rbpi():
            import RPi.GPIO as GPIO
            from io_thread.button_handler import ButtonHandler
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.settings.physical_button_pin, GPIO.IN)
            cb = ButtonHandler(self.settings.physical_button_pin, self.button_handler, bouncetime=100)
            cb.start()
            GPIO.add_event_detect(self.settings.physical_button_pin, GPIO.RISING, callback=cb)

        while True:
            time.sleep(0.1)

            # simulation
            #if random.random() < 0.01:
            #    print("Button short press simulated")
            #    self.trigger_short_press()
            #elif random.random() > 0.99:
            #    print("Button long press simulated")
            #    self.trigger_long_press()



    @staticmethod
    def is_rbpi():
        return os.uname()[4][:3] == 'arm'

    def button_handler(self, duration):
        print("Physical button pressed with duration: " + duration)

        if duration > self.settings.physical_button_longpress_duration:
            self.trigger_long_press()
        else:
            self.trigger_short_press()

    def trigger_long_press(self):
        for handler in self.thread_context.button_long_press_handlers:
            handler()

    def trigger_short_press(self):
        for handler in self.thread_context.button_short_press_handlers:
            handler()




