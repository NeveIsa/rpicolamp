import fastapi
import ldr2pix

app = fastapi.FastAPI()

@app.get("/npix/")
def npix(n:int,fg:str,bg:str='black'):
    result, reply = ldr2pix.npixfill(n,fg,bg)
    return reply

@app.get("/ldr/")
def ldr():
    result, reply = ldr2pix.ldr()
    return reply


