import pygame
import threading
import datetime


class KeyboardDebouncer(threading.Thread):
    def __init__(self, pygame, key_codes, func, bouncetime=50):
        super().__init__(daemon=True)
        self.pygame = pygame
        self.func = func
        self.key_codes = key_codes
        self.bouncetime = float(bouncetime) / 1000
        self.last_val = self.get_key_value()
        self.press_time = datetime.datetime.now
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self):
        now = datetime.datetime.now()
        key_val = self.get_key_value()

        if key_val == 1 and self.last_val == 0:
            self.press_time = now

        if key_val == 0 and self.last_val == 1:
            ms = int((now - self.press_time).total_seconds() * 1000)
            self.func(ms)

        self.last_val = key_val
        self.lock.release()

    def get_key_value(self):
        keys = self.pygame.key.get_pressed()
        for key_code in self.key_codes:
            if keys[key_code]:
                return 1

        return 0





