import http.client
import json
import datetime
import time
conn = http.client.HTTPConnection("catalog.cse.nd.edu", port=9097)
conn.request("GET", "/query.json")

response = conn.getresponse()
data = response.read()
response_data = json.loads(data)
print(response_data)
for server in response_data:
    if "owner" in server.keys():
        if server["owner"] == "tmasasa":
            print(server)




        
    
    
       
       
      
       

       
           