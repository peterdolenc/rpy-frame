import RPi.GPIO as GPIO
import threading
import datetime


class GpioButtonHandler(threading.Thread):
    def __init__(self, pin, func, bouncetime=100):
        super().__init__(daemon=True)

        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime) / 1000
        self.lastpinval = GPIO.input(self.pin)
        self.lastpintime = datetime.datetime.now
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, start_time):
        now = datetime.datetime.now()
        pinval = GPIO.input(self.pin)

        if pinval == 1 and self.lastpinval == 0:
            self.lastpintime = now

        if pinval == 0 and self.lastpinval == 1:
            ms = int((now - self.lastpintime).total_seconds() * 1000)
            self.func(ms)

        self.lastpinval = pinval
        self.lock.release()





