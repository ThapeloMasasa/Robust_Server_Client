import socket
import sys
import json
import os
import copy
import time
from datetime import datetime
from hashTable1 import HashTable

hashtable = HashTable()

class Server:
    def __init__(self,table):
        self.host = socket.getfqdn()
        self.servername = sys.argv[1]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 0))
        _, self.port = self.server.getsockname()
        self.server.listen()
        self.conn = None
        self.addr = None
        self.mem_table = table
        self.log_length = 0
        self.timer = time.time()
        self.counter = 1
        #check if server just initialized
        self.just_init = True

   
    def make_udp_conn(self):
        print("this is the host, ",self.host)
        name_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.counter += 1
        message ={
            "type": "hashtable",
            "owner": "tmasasa",
            "port": self.port,
            "project": self.servername
        }
        byte_data = json.dumps(message).encode('utf-8')
        name_server.sendto(byte_data, ("catalog.cse.nd.edu", 9097))

    def accept_connection(self):
        print(f"Listening for connections on port {self.port}")
        self.conn, self.addr = self.server.accept()
        print(f"Accepted connection from {self.addr}")
        self.conn.send("Connection established".encode("utf-8"))
    #update log with each remove or insert made
    def add_to_log(self, data):
        
        log = []
        now = datetime.now()

        cur_time = now.strftime("%H:%M:%S")
        log.append(cur_time)
        if data["method"] == "insert":
            log.append(data["method"])
            log.append(data["key"])
            log.append(data["value"])
        elif data["method"] == "remove":
            log.append(data["method"])
            log.append(data["key"])    
        log.append("\n")      
        store = ' '.join([str(elem) for elem in log])
        
        f = open("table.txn", "a+")
        f.write(store)
        f.flush()
        os.fsync(f.fileno())
        f.close()
        
    #handle incoming requests
    def handleRequests(self):
        self.just_init = False   
        while True:
            new_time = time.time()
            #if a minute passes, send update to name server
            if ((self.timer - new_time) >= 60):
                self.make_udp_conn()
                self.timer = time.time()
            data = b''
            tmp_data = self.conn.recv(1024)
            #if now data received   
            if not tmp_data:
                continue
            data+= tmp_data
            data = data
            unserialized_data = json.loads(data.decode('utf-8'))
            if unserialized_data["method"] == "insert": 
                self.add_to_log(unserialized_data)
                self.log_length += 1 
                if self.log_length >= 100:
                    self.update_checkpoint()
                    self.log_length = 0
                self.mem_table.insert(unserialized_data["key"], unserialized_data["value"])
                response = {"message": "Value inserted"}
                byte_data = json.dumps(response).encode('utf-8') 
                self.conn.sendall(byte_data)
                
            elif unserialized_data["method"] == "remove":
                self.add_to_log(unserialized_data)
                self.log_length += 1 
                if self.log_length >= 100:
                    self.update_checkpoint()
                    self.log_length = 0
                self.mem_table.remove(unserialized_data["key"])
                response = {"message": "Item Removed"}
                byte_data = json.dumps(response).encode('utf-8') 
                self.conn.sendall(byte_data)
            elif unserialized_data["method"] == "lookup":
                value = self.mem_table.lookup(unserialized_data["key"])
                response = {"message": "Value looked up", "value": value, "status": False}
                byte_data = json.dumps(response).encode('utf-8') 
                self.conn.sendall(byte_data)
            elif unserialized_data["method"] == "findSize":
                value= self.mem_table.size()
                response = {"message": "Size found", "value": value}
                byte_data = json.dumps(response).encode('utf-8') 
                self.conn.sendall(byte_data)

            elif unserialized_data["method"] == "query":
               value = self.mem_table.query(unserialized_data["subkey"], unserialized_data["subvalue"])
               response = {"message":"Table Quired for data", "value": value}
               byte_data = json.dumps(response).encode('utf-8') 
               self.conn.sendall(byte_data)
        
    #create check point upon initiallization
    def update_checkpoint(self):
        
        data = self.mem_table.getValues()
        
        directory = os.getcwd() 
        temp_checkpoint = copy.copy(directory+"/table.ckpt")
        file = directory+"/table.ckpt"
        
        
        for item in data:
            temp_data = ':'.join([str(elem) for elem in item])
            f = open("table.ckpt", "a+")
            f.write(temp_data+"\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()
        os.rename(temp_checkpoint,file)
        #truncate the transaction log
        open("table.txn", 'w').close()
       
        
    #run log to bring table up to date
    def run_log(self):
      
        log_data = []
        f = open("table.txn", "r")
        for line in f.readlines():
            temp_store = []
            data = line.split(" ")
            for i in range(1,len(data)):
                temp_store.append(data[i])
                
                if data[1] == "insert":
                    print("time",data[0],"method", data[1], "key ",data[2], "value", data[3] )
                    self.mem_table.insert(data[2], data[3])
                elif data[1] == "remove":
                   # print("Init run log removed key ", data[2])
                    self.mem_table.remove(data[2])
        self.update_checkpoint()
            
            
        f.close()
        return log_data
    def read_checkpoint(self):
        f = open("table.ckpt", "r")
        for line in f.readlines():
            data = line.split(":")
            #update the table with current checkpoint state
            if len(data)> 1:
                self.mem_table.insert(data[0],data[1])
            
           
        f.close()
    
    
        
    #update state to  new values    
    def check_init_state(self):
        #send state to name server
        self.make_udp_conn()
        directory = os.getcwd() 
        if os.path.isfile(directory+"/table.txn") and os.path.isfile(directory+"/table.ckpt"):
            #check if the checkpoint file is empty
            if (os.stat(directory+"/table.ckpt").st_size > 0 or os.stat(directory+"/table.txn").st_size > 0) and self.just_init:
                #read checkpoint state into memory  and update with available contents of the file
                self.run_log()
                self.read_checkpoint()
                
            else:
                self.update_checkpoint()
            
        else:
            #create empty checkpoint 
            f = open("table.ckpt", "a+")
            f.flush()
            os.fsync(f.fileno())
            f.close()
            #create empty transaction log
            f = open("table.txn", "a+")
            f.flush()
            os.fsync(f.fileno())
            f.close()
            
        
        
        
               
    
if __name__ == "__main__":
    serverInstance = Server(hashtable)
    serverInstance.check_init_state()
    serverInstance.accept_connection()
    serverInstance.handleRequests()
    
    
    
    
   

