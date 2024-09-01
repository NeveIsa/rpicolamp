import socket
import json
from random import randint
from time import sleep
import sys

HOST,PORT = "PicoW.lan",1234
addr = (HOST,PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2)

class RPC:
    def __init__(self, method="list_rpc"):
        self.method =  method

    def __call__(self, *params, reply=False):
        msgID = randint(100,1000)
        s.sendto(json.dumps({"id":msgID, "method":self.method, "params": params}).encode(), addr)

        try: reply,__addr = s.recvfrom(1024)
        except: 
            # print("UDP received timeout - device might be down!")
            return None, {"info":"udp recv timeout"}
            sleep(2)
            
        reply = json.loads(reply)
        if reply["id"]!=msgID:
            reply["moreinfo"] = "msgID don't match, sent_id:{msgID} , recv_id:{reply['id:']}"
            return None, reply
        result = reply["result"] if "result" in reply else None
        return result, reply

ldr = RPC("read_ldr")
npixfill = RPC("write_npix")

if __name__=="__main__":

    if len(sys.argv) > 1:
        result, reply = npixfill(3, *sys.argv[1:])    
        print(result)
        exit(0)

    delay = 1
    while True:
        level, reply = ldr()
        if level:
            level = level // 2**5
            result, reply = npixfill(8-level, "gray", "black")
            sleep(delay)
        print(reply)
