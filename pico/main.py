import dev
from time import sleep
from colors import colors
from random import randrange
import net
import udp
from math import sin,cos, pi
import machine 

rpc = udp.RPC()
ldr = dev.LDR()
npix = dev.NPIX()


@rpc.register
def list_rpc():
    return list(rpc.functions)

@rpc.register
def read_ldr():
    return ldr()

@rpc.register
def write_npix(level, active_color=(255,255,255), inactive_color=(0,0,0)):
    if type(active_color)==str:
        if not active_color in colors:
            active_color = "white"
        active_color = colors[active_color]

    if type(inactive_color)==str:
        if not inactive_color in colors:
            inactive_color = "black"
        inactive_color = colors[inactive_color]
    
    return npix.fill(level, active_color, inactive_color)

@rpc.register
def intro():
    delay = 0.025
    tricolor = ["DarkOrange", "DarkOrange","white", "blue","white","green","green","green"]
    tricolor = [colors[c] for c in tricolor]
    for i in range(101):
        npix.raw( buffer = tricolor, alpha=abs(sin(2*i*pi/100)) )
        sleep(delay)

    # reset to dark, and set aplha = 1
    npix.raw(buffer=[(0,0,0)]*8, alpha=1.0)


@rpc.register
def reset(hard=1):
    if hard: machine.reset()
    else: machine.soft_reset()

def loop():
    while True: rpc.handle()

intro()
if __name__=="__main__":
    loop()
