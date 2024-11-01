import socket
from conf import conf
import json

IP = "0.0.0.0"
PORT = conf["UDP"]["PORT"]

class RPC:
    def __init__(self): 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP,PORT))
        self.functions = {}

    def register(self, func):
        self.functions[func.__name__] = func
        return func

    def handle(self):
        data, addr = self.sock.recvfrom(1024)
        try: 
            payload = json.loads(data)
            payload["note"] = ""
        except:
            payload = {"note":""}
            payload["note"] += "| invalid JSON format |"
        finally:
            if type(payload) != dict: payload = {"note":""}

        if not "method" in payload:
            payload["note"] += "| missing JSON key 'method' |"
            method = ""
        else:
            method = payload["method"]
            # del payload["method"]
        
        if not "params" in payload:
            params = []
            payload["note"] += "| Warning: missing JSON key 'params' |"
        else: 
            params = payload["params"]
            # del payload["params"]
        
        if not type(params) == list:
            payload["note"] += "| 'params' key in JSON is not a list |"

        if method=="":
            pass
        elif not method in self.functions:
            payload["note"] += "| method not found in registry |" 
        else:
            try:
                payload["result"] = self.functions[method](*params)
            except:
                payload["note"] += f"| Exception calling {method}(*{params}) |"

        # write results back
        self.sock.sendto(json.dumps(payload), addr)


    def close(self):
        self.sock.close()

    def __del__(self):
        self.close()
