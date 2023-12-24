import socket

import datetime
import threading



class Logger:
    def __init__(self):
        pass
    def info(self, message):
        print(f"[{datetime.datetime.now()}] [INFO] {message}")
    def warn(self, message):
        print(f"[{datetime.datetime.now()}] [WARN] {message}")
    def debug(self, message):
        print(f"[{datetime.datetime.now()}] [DEBUG] {message}")
    def error(self, message):
        print(f"[{datetime.datetime.now()}] [ERROR] {message}")



class Server:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.protocol_list = {}
        self.running = True
        self.logger = Logger()
        self.client_list = []
        self.setting = {
            "max_client" : 10
        }
    def config(self, key, value):
        if self.setting.get(key):
            self.setting[key] = value

    def add_protocol(
        self, 
        protocol: str, 
        func):
        self.protocol_list[protocol] = func
    def run(self, check_with_log:bool=True):
        while self.running:
            try:
                
                
                self.sock.listen(self.setting["max_client"])
                conn, addr = self.sock.accept()
                if check_with_log:
                    self.logger.info(f"New Client Connected. Starting New Thread. IP and Port : {addr}")
                    self.logger.info(f"Number of Client : {len(self.client_list)}")
                    threading.Thread(target=self.thread,args=(conn, addr, check_with_log,)).start()
                
                self.client_list.append(conn)
                
                    
                    
            except Exception as e:
                
                self.logger.error(f"Exception :{e.with_traceback()}")
    def thread(self, conn, addr, check_with_log):
        self.logger.info("Thread started")
        while self.running:
            data = conn.recv(1024)
            if not data:
                if check_with_log:
                    self.logger.info(f"Connection closed: {addr}")
                break
            msg = data.decode()
            protocol_Data = msg.split("__")
            self.protocol_list.get(protocol_Data[0])(protocol_Data[1])

                


    def send(self, protocol, data):
        for conn in self.client_list:
            sending = protocol + "__" + data
            conn.send(sending.encode())
   

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.protocol_list = {}
        self.running = True
        self.logger = Logger()
        self.client_list = []
        self.setting = {
            
        }
    def config(self, key, value):
        if self.setting.get(key):
            self.setting[key] = value
    def recive(self):
        data = self.sock.recv(1024)
        msg = data.decode('utf-8')
        protocol_data = msg.split("__")
        return {"Protocol": protocol_data[0], "data":protocol_data[1]}
    def send(self, protocol, data):
        sending = protocol + "__" + data

        self.sock.send(sending.encode())
    
            
                








