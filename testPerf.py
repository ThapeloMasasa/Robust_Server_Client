import time
import sys
from HashTableClient import Client
array = [    ("book", "desk"),    ("tree", "grass"),    ("car", "bus"),    ("coffee", "tea"),    ("dog", "cat"),    ("phone", "computer"),    ("table", "chair"),    ("television", "radio"),    ("pencil", "paper"),    ("water", "juice"),    ("music", "dance"),    ("food", "drink"),    ("shirt", "pants"),    ("house", "apartment"),    ("sun", "moon"),    ("cloud", "sky"),    ("ocean", "beach"),    ("mountain", "valley"),    ("person", "animal"),    ("friend", "family"),    ("day", "night"),    ("summer", "winter"),    ("flower", "tree"),    ("love", "hate"),    ("fast", "slow"),    ("big", "small"),    ("hot", "cold"),    ("happy", "sad"),    ("long", "short"),    ("old", "new"),    ("good", "bad"),    ("right", "wrong"),    ("strong", "weak"),    ("heavy", "light"),    ("rich", "poor"),    ("easy", "hard"),    ("high", "low"),    ("near", "far"),    ("young", "old"),    ("fast", "slow"),    ("new", "old"),    ("first", "last"),    ("start", "finish"),    ("open", "close"),    ("begin", "end"),    ("above", "below"),    ("inside", "outside"),    ("up", "down"),    ("left", "right"),    ("over", "under"),    ("front", "back"),    ("top", "bottom"),    ("empty", "full"),    ("happy", "sad"),    ("big", "small"),    ("fast", "slow"),    ("hot", "cold"),    ("heavy", "light"),    ("rich", "poor"),    ("easy", "hard"),    ("high", "low"),    ("near", "far"),    ("young", "old"),    ("fast", "slow"),    ("new", "old"),    ("first", "last"),    ("start", "finish"),    ("open", "close"),    ("begin", "end"),    ("above", "below"),    ("inside", "outside"),    ("up", "down"),    ("left", "right"),    ("over", "under"),    ("front", "back"),    ("top", "bottom"),    ("empty", "full"),    ("happy", "sad")]
array = array*5


ht = Client(sys.argv[1])
ht.get_server()
ht.establish_connection()
#insertion perfomance
start = time.perf_counter()
for tuple in array:
    ht.insert(tuple[0],tuple[1])

end = time.perf_counter()

throughput = 500/(end - start)
latency = 1/(500/(end - start))
print(f"The throughput for insertion in this outlier {throughput}")
print(f"The latency for insertion in this outlier is {latency}")


#lookup perfomance
start = time.perf_counter()
for tuple in array:
    ht.lookup(tuple[0])

end = time.perf_counter()

throughput = 500/(end - start)
latency = 1/(500/(end - start))
print(f"The throughput for lookup in this is {throughput}")
print(f"The latency for lookup in this is {latency}")

time.sleep(3)
#query perfomance
start = time.perf_counter()
for tuple in array:
    ht.query(tuple[0],tuple[1])

end = time.perf_counter()

hroughput = 500/(end - start)
latency = 1/(500/(end - start))
print(f"The throughput for query in this is  {throughput}")
print(f"The latency for query in this is {latency}")

time.sleep(3)
#remove perfomance
start = time.perf_counter()
for tuple in array:
    ht.remove(tuple[0])

end = time.perf_counter()

hroughput = 500/(end - start)
latency = 1/(500/(end - start))
print(f"The throughput for remove in this is {throughput}")
print(f"The latency for  remove in this is {latency}")

time.sleep(3)
start = time.perf_counter()
for tuple in array:
    ht.size()

end = time.perf_counter()

hroughput = 500/(end - start)
latency = 1/(500/(end - start))
print(f"The throughput for findsize in this is {throughput}")
print(f"The latency for findsize in this isis {latency}")

ht.close()

