class HashTable:

    def __init__(self) -> None:
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value
        

    def lookup(self,key):
        if key in self.table.keys():
            return  self.table[key] 
        
    
    def remove(self, key):
        if key in self.table.keys():
            del self.table[key]
            return True
        else:
            return False
    def size(self):
        return len(self.table)
    def query(self, subkey, subvalue):
        ans = []
        for key, value in self.table.items():
            if isinstance(value, dict):
                if subkey in value.keys():
                    if subvalue == value[subkey]:
                        temp_ans = (key, value)
                        ans.append(temp_ans)
        return ans
    def getValues(self):
        array = []
        for key, value in self.table.items(): 
            array.append([key, value])
            
        return array
                    


    

