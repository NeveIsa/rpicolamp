from dev import *
from time import sleep

class Task:
    def __init__(self):
        self.ldr = LDR()
        self.npix = NPIX()
    def __call__(self):
        level = self.ldr()//8
        self.npix.fill(8-level)
        sleep(0.25)

