import socket
import json
import sys
import http.client
import time
class Client:
    def __init__(self, name):
        self.port = None
        self.host = name
        self.servername = "tmasasa-a4"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timer = 0
        self.lastsend = 0
        
        
    def get_server(self):
        # keep retrying until the right port is found for the right server 
            try:
                conn = http.client.HTTPConnection("catalog.cse.nd.edu", port=9097)
                conn.request("GET", "/query.json")
                response = conn.getresponse()
                if response.status != 200:
                    print("unsuccessful Response... retrying..")
                    time.sleep(2)
                    return False
                data = response.read()
                response_data = json.loads(data)
                
                for server in response_data:
                    if "project" in server.keys():
                        if server["project"] == self.servername:
                            if server["lastheardfrom"] > self.lastsend:
                                self.port = int(server["port"])
                                self.lastsend = server["lastheardfrom"]
                return True
            except http.client.HTTPException:
                print("Failed to lookup server.. Retrying..")
                time.sleep(2)
                return False
        
        
       
           
           
    # Establish connection         
    def establish_connection(self):
        delay = 2
        while True:
            while True:
                serverFound = self.get_server()
                if serverFound:
                    break
            try:
                print("This is the host and port", self.host, self.port)
                print(type(self.host), type(self.port))
                try:
                    self.client.connect((self.host, self.port))
                    message = self.client.recv(1024).decode("utf-8")
                    print(message)
                    break
                except OSError:
                    self.close()
                    print("Reconnecting... OSerror caught")
                    time.sleep(delay)
                    delay *= 2  
            except BrokenPipeError:
                self.close()
                print("Reconnecting... Broken Pipe")
                time.sleep(delay)
                delay *= 2  
            
            except ConnectionError:
                print("Reconnecting... Connect error caught")
                time.sleep(delay)
                delay *= 2  
    
        
    def redo_reception(self,method):
        data = ""
        delay = 2
        while not data:
            self.redo_request(method)
            self.client.settimeout(5)
            try:
                data = self.client.recv(1024)
            except socket.timeout:
                print("Reconnecting... response took too long")
                time.sleep(delay)
                delay *= 2  
                self.establish_connection()
                
        return data
        
        
        
    def redo_request(self, request):
        
        if request[0] == "insert":
            print("Reconnecting... retrying insert")
            key = request[1]
            value = request[2]
            message = {"method": 'insert', "key": key, "value" : value}
            byte_data = json.dumps(message).encode('utf-8')
            delay = 2
            while True:
                try:
                    self.client.sendall(byte_data)
                    break
                except BrokenPipeError:
                    self.close()
                    print("Reconnecting.. Broken Pipe... retrying to find size")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection() 
                except ConnectionError:
                    print("Reconnecting... retrying insert")
                    time.sleep(delay)
                    delay *= 2  
                    self.establish_connection()
                except OSError:
                    self.close()
                    print("Reconnecting.. OSerror... retrying to find size")
                    time.sleep(3)
                    delay *= 2 
                    self.establish_connection() 
        elif request[0] == "lookup":
            key = request[1]
            message = {"method": 'lookup', "key": key}
            byte_data = json.dumps(message).encode('utf-8') 
            delay = 2
            while True:
                try:
                    self.client.sendall(byte_data)
                    break
                except BrokenPipeError:
                    self.close()
                    print("Reconnecting.. Broken Pipe... retrying to find size")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection() 
                except ConnectionError:
                    print("Reconnecting... retrying lookup")
                    time.sleep(delay)
                    delay *= 2  
                    self.establish_connection()
                except OSError:
                    self.close()
                    print("Reconnecting.. OSerror... retrying to find size")
                    time.sleep(3)
                    delay *= 2 
                    self.establish_connection() 
        elif request[0] == "remove":
            key = request[1]
            message = {"method": 'remove', "key": key}
            byte_data = json.dumps(message).encode('utf-8') 
            delay = 2
            while True:
                try:
                    self.client.sendall(byte_data)
                    break
                except BrokenPipeError:
                    self.close()
                    print("Reconnecting.. Broken Pipe... retrying to find size")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection() 
                except ConnectionError:
                    print("Reconnecting... retrying remove")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection() 
                except OSError:
                    self.close()
                    print("Reconnecting.. OSerror... retrying to find size")
                    time.sleep(3)
                    delay *= 2 
                    self.establish_connection() 
        elif request[0] == "query":
            subkey = request[1]
            subvalue = request[2]
            message = {"method": "query", "subkey":subkey, "subvalue": subvalue}
            byte_data = json.dumps(message).encode('utf-8') 
            delay = 1
            while True:
                try:
                    self.client.sendall(byte_data)
                    break
                    
                except BrokenPipeError:
                    self.close()
                    print("Reconnecting.. Broken Pipe... retrying to find size")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection() 
                except ConnectionError:
                    print("Reconnecting... retrying query")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection()
                except OSError:
                    self.close()
                    print("Reconnecting.. OSerror... retrying to find size")
                    time.sleep(3)
                    delay *= 2 
                    self.establish_connection() 
        elif request[0] == "findSize":
            delay = 2
            while True:
                try:
                    self.client.sendall(byte_data)
                    break
                except BrokenPipeError:
                    self.close()
                    print("Reconnecting.. Broken Pipe... retrying to find size")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection() 
                except ConnectionError:
                    print("Reconnecting... retrying to find size")
                    time.sleep(delay)
                    delay *= 2 
                    self.establish_connection() 
                except OSError:
                    self.close()
                    print("Reconnecting.. OSerror... retrying to find size")
                    time.sleep(3)
                    delay *= 2 
                    self.establish_connection() 
            
             
     
        
    #Insert into the server
    def insert(self,key,value):
        #check for if arguemtns are correct:
        checkKey = isinstance(key, str)
        if not checkKey:
            return "Key must be string"
        else:
            if len(key) < 1:
                    return "Key cant be empty String"
            message = {"method": 'lookup', "key": key}
            byte_data = json.dumps(message).encode('utf-8') 
            
            try:
                self.client.sendall(byte_data)
            except socket.error:
                time.sleep(2)
                self.establish_connection()
                self.redo_request(["lookup", key])
           
            self.client.settimeout(5)
            try:
                data = self.client.recv(1024)
            except socket.timeout():
                self.establish_connection()
                data = self.redo_reception(["insert", key, value])
            except ConnectionError:
                self.establish_connection()
                data = self.redo_reception(["insert", key, value])
            if not data:
                data = self.redo_reception(["insert", key, value])
            unserialized_data = json.loads(data.decode('utf-8'))
            return unserialized_data["message"]
    #Remove the data
    def remove(self,key):
        checkKey = isinstance(key, str)
        if not checkKey:
            return "Key Must be string"
        else:
            if len(key) < 1:
                    return "Key cant be empty String"
            message = {"method": 'lookup', "key": key}
            byte_data = json.dumps(message).encode('utf-8') 
            
            try:
                self.client.sendall(byte_data)
            except socket.error:
                time.sleep(2)
                self.establish_connection()
                self.redo_request(["remove", key])
           
            self.client.settimeout(5)
            try:
                data = self.client.recv(1024)
            except socket.timeout():
                self.establish_connection()
                data = self.redo_reception(["remove", key])
            except ConnectionError:
                self.establish_connection()
                data = self.redo_reception(["remove", key])
            if not data:
                data = self.redo_reception(["remove", key])
            unserialized_data = json.loads(data.decode('utf-8'))
            return unserialized_data["message"]
            
    #lookup the data
    def lookup(self,key):
        checkKey = isinstance(key, str)
        if not checkKey:
            return " Key must be string"
        else:
            if len(key) < 1:
                return "Key cant be empty String"
            message = {"method": 'lookup', "key": key}
            byte_data = json.dumps(message).encode('utf-8') 
            
            try:
                self.client.sendall(byte_data)
            except socket.error:
                time.sleep(2)
                self.establish_connection()
                self.redo_request(["lookup", key])
           
            self.client.settimeout(5)
            try:
                data = self.client.recv(1024)
            except socket.timeout():
                self.establish_connection()
                data = self.redo_reception(["lookup", key])
            except ConnectionError:
                self.establish_connection()
                data = self.redo_reception(["lookup", key])
            if not data:
                data = self.redo_reception(["lookup", key])
            unserialized_data = json.loads(data.decode('utf-8'))
            return unserialized_data["message"]
            
    #Get the size of the hashtable
    def size(self):
        message = {"method": 'findSize'}
        byte_data = json.dumps(message).encode('utf-8')     
        try:
            self.client.sendall(byte_data)
        except socket.error:
            time.sleep(2)
            self.establish_connection()
            self.redo_request(["findSize"])
            
        self.client.settimeout(5)
        try:
            data = self.client.recv(1024)
        except socket.timeout():
            self.establish_connection()
            data = self.redo_reception(["findSize"])
        except ConnectionError:
            self.establish_connection()
            data = self.redo_reception(["findSize"])
        if not data:
            data = self.redo_reception(["findSize"])
        unserialized_data = json.loads(data.decode('utf-8'))
        return unserialized_data["message"]    
            
    
    
    #query the hashtable
    def query(self, subkey, subvalue):
        checkKey = isinstance(subkey, str)
        if not checkKey:
            return " Key must be string"
        else:
            if subkey == "":
                return "Key cant be empty"
            message = {"method": 'query', "subkey": subkey, "subvalue": subvalue}
            byte_data = json.dumps(message).encode('utf-8') 
            
            try:
                self.client.sendall(byte_data)
            except socket.error:
                time.sleep(2)
                self.establish_connection()
                self.redo_request(["query", subkey, subvalue])
           
            self.client.settimeout(5)
            try:
                data = self.client.recv(1024)
            except socket.timeout():
                time.sleep(2)
                self.establish_connection()
                data = self.redo_reception(["query", subkey, subvalue])
            except ConnectionError:
                time.sleep(2)
                self.establish_connection()
                data = self.redo_reception(["query", subkey, subvalue])
            if not data:
                data = self.redo_reception(["query", subkey, subvalue])
            unserialized_data = json.loads(data.decode('utf-8'))
            return unserialized_data["message"]
            
    def close(self):
        self.client.close()
        time.sleep(5)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    


