from machine import Pin, ADC
from conf import conf
import neopixel
from math import floor

if "PINS" in conf:
    PINS = conf["PINS"]
    if "LDR" in PINS: ldr_pin = Pin(PINS["LDR"])
    if "NPIX" in PINS: npix_pin = Pin(PINS["NPIX"])


class LDR:
    def __init__(self):
        self.adc = ADC(ldr_pin)
    def __call__(self):
        return self.adc.read_u16()//2**8


class NPIX:
    def __init__(self):
        self.PIXCOUNT = 8
        self.npixels = neopixel.NeoPixel(npix_pin, self.PIXCOUNT)
        self.buffer = [(255,255,255)]*self.PIXCOUNT
        self.alpha = 1.0
        
    def fill(self, n, active_color=[255,255,255], inactive_color=[0,0,0]):
        for i in range(self.PIXCOUNT):
            self.buffer[i] = active_color if i < n else inactive_color
        self._draw()

    def _draw(self):
        upto = self.PIXCOUNT
        for i in range(upto):
            self.npixels[i] = tuple(  map(lambda x: floor(self.alpha*x) if x>0 else 0, self.buffer[i])    )
        self.npixels.write()
    
    def raw(self,buffer, alpha=1.0):
        n = min(len(buffer), len(self.buffer))
        self.buffer[:n] = buffer[:n]  
        self.alpha = alpha
        self._draw()

__all__ = ["LDR", "NPIX"]
    


