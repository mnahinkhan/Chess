import pickle
from collections import defaultdict
openings = defaultdict(list)
try:
    file_handle = open('openingTable.txt','r+')
    openings = pickle.loads(file_handle.read())
except:
    file_handle = open('openingTable.txt','w')


key = ((('Rb', 0, 'Bb', 'Qb', 'Kb', 'Bb', 0, 'Rb'), ('Pb', 'Pb', 0, 'Pb', 0, 'Pb', 'Pb', 'Pb'), (0, 0, 'Nb', 0, 0, 'Nb', 0, 0), (0, 0, 0, 0, 'Pb', 0, 0, 0), (0, 0, 0, 0, 'Pw', 0, 0, 0), (0, 'Nw', 'Nw', 0, 0, 0, 0, 0), ('Pw', 'Pw', 'Pw', 0, 0, 'Pw', 'Pw', 'Pw'), ('Rw', 0, 'Bw', 'Qw', 'Kw', 'Bw', 0, 'Rw')), 1, ((True, True), (True, True)))

del openings[key]

file_handle.seek(0)
pickle.dump(openings,file_handle)
file_handle.truncate()
file_handle.close()
