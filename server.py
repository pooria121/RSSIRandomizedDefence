import simplejson as json
import socket
import sys
from threading import Lock, Thread

import numpy as np

from scipy import stats 


class PhyscIDS:
    P_VALUE = 0.05
    N_L_HISTORICAL = 5
    profile = {}
    trusted_dist = None

    def __init__(self, historical):
        self.trusted_dist = historical

    def record(self, mac, value):
        if mac in self.profile:
            self.profile[mac] = np.append(self.profile[mac], [value])
        else:
            self.profile[mac] = np.asarray([value])

    def filter(self, mac, value):
        lst_prf = np.append(self.profile[mac][-self.N_L_HISTORICAL:], [value]) 
        p_test =  stats.ks_2samp(self.trusted_dist, lst_prf)
        return p_test[1] > self.P_VALUE,p_test[1]

records = []
lock = Lock()
counter = 0
sender_mac = '0A-AA-00-00-00-01'
receiver_mac = '0A-AA-00-00-00-02'

nodes = {'Sender':PhyscIDS(np.fromfile('r_sender')),
        'Receiver':PhyscIDS(np.fromfile('r_sender'))}



def node_thread(c):
    global counter
    global nodes

    counter += 1
    data = ''
    while True:

        # data received from client
        try:
            i = c.recv(1024)

            if not i:
                break
            data += str(i)

        except:
            break
    obj = json.loads(str(data))
    
    
    try:
        lock.acquire()  # will block if lock is already held
        node_id = obj['nodeID']
        if node_id != 'Adversary':
            node_ids = nodes[node_id]
            node_ids.record(obj['src'],obj['power'])
            flag,p_val = node_ids.filter(obj['src'],obj['power'])
            obj[u'flag'] = (bool)(flag)
            obj[u'p_value'] = p_val
        records.append(obj)
    finally:          
        print('connection is now closed!')
        c.close()
        print(obj)
        lock.release()      


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
print('now it begins!')
sock.listen(1)
try:
    while counter < 1000:
        connection, client_address = sock.accept()
        Thread(target=node_thread, args=(connection,)).start()
finally:
    sock.close()
    with open(sys.argv[1], 'w') as outfile:
        json.dump(records, outfile)