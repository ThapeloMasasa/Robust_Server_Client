import sys
from HashTableClient import Client



ht = Client(sys.argv[1])
ht.get_server()
ht.establish_connection()
#evaluate insert function
ht.insert("1", "Masasa")
ht.insert("2", "Gerry")
ht.insert("1", "Ntando")
ht.insert(2, "Bangene")
ht.insert([1,2,3,4],{"num1":2,"num2":3})
ht.insert("3", "Bangene")

#evaluate lookup
value = ht.lookup("1")
print(value)
value = ht.lookup("2")
print(value)
value = ht.lookup(1)
print(value)
value = ht.lookup("")
print(value)

#evaluate remove
ht.remove("2")
ht.remove("2")
ht.remove(1)
ht.remove("")
value = ht.lookup("1")
print(value)
value = ht.lookup("2")
print(value)

#evaluate size
value = ht.size()
print(value)
ht.insert("new","addMore")
value= ht.size()
print(value)

#evaluate the query
value = ht.query("bob", "jones")
print(value)
ht.insert("Jetski", {"bob":"jones", "snack":"doritos"})
value = ht.query("bob", "jones")
print(value)

#close the socket
ht.close()











