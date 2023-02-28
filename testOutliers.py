import time
import sys
from HashTableClient import Client
array = [    ("book", "desk"),    ("tree", "grass"),    ("car", "bus"),    ("coffee", "tea"),    ("dog", "cat"),    ("phone", "computer"),    ("table", "chair"),    ("television", "radio"),    ("pencil", "paper"),    ("water", "juice"),    ("music", "dance"),    ("food", "drink"),    ("shirt", "pants"),    ("house", "apartment"),    ("sun", "moon"),    ("cloud", "sky"),    ("ocean", "beach"),    ("mountain", "valley"),    ("person", "animal"),    ("friend", "family"),    ("day", "night"),    ("summer", "winter"),    ("flower", "tree"),    ("love", "hate"),    ("fast", "slow"),    ("big", "small"),    ("hot", "cold"),    ("happy", "sad"),    ("long", "short"),    ("old", "new"),    ("good", "bad"),    ("right", "wrong"),    ("strong", "weak"),    ("heavy", "light"),    ("rich", "poor"),    ("easy", "hard"),    ("high", "low"),    ("near", "far"),    ("young", "old"),    ("fast", "slow"),    ("new", "old"),    ("first", "last"),    ("start", "finish"),    ("open", "close"),    ("begin", "end"),    ("above", "below"),    ("inside", "outside"),    ("up", "down"),    ("left", "right"),    ("over", "under"),    ("front", "back"),    ("top", "bottom"),    ("empty", "full"),    ("happy", "sad"),    ("big", "small"),    ("fast", "slow"),    ("hot", "cold"),    ("heavy", "light"),    ("rich", "poor"),    ("easy", "hard"),    ("high", "low"),    ("near", "far"),    ("young", "old"),    ("fast", "slow"),    ("new", "old"),    ("first", "last"),    ("start", "finish"),    ("open", "close"),    ("begin", "end"),    ("above", "below"),    ("inside", "outside"),    ("up", "down"),    ("left", "right"),    ("over", "under"),    ("front", "back"),    ("top", "bottom"),    ("empty", "full"),    ("happy", "sad")]
array = array*10


ht = Client(sys.argv[1])
ht.get_server()
ht.establish_connection()

#insertion perfomance
min_time = float('inf')
max_time = 0
for tuple in array:
    start = time.perf_counter()
    ht.insert(tuple[0],tuple[1])
    end = time.perf_counter()
    diff = end - start
    if diff > max_time:
        max_time = diff
    if diff < min_time:
        min_time = diff



print(f"The highest for inmserton in this outlier {max_time}")
print(f"The lowest  for insertion in this outlier is {min_time}")

#Removal perfomance
min_time = float('inf')
max_time = 0
for tuple in array:
    start = time.perf_counter()
    ht.remove(tuple[0])
    end = time.perf_counter()
    diff = end - start
    if diff > max_time:
        max_time = diff
    if diff < min_time:
        min_time = diff

print(f"The highest for removal in this outlier {max_time}")
print(f"The lowest  for removal in this outlier is {min_time}")