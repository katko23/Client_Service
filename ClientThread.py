import random
from threading import Thread
import Setings
import threading
import requests

class Client(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id_client = id
        self.name = "Client" + str(id)
        self.waiting = False

    host = Setings.hostName
    port = Setings.serverPort

    def run(self):
        while True:
            if self.waiting == False:
                nr_of_items = random.randint(1,Setings.max_nr_of_items)
                order_items = []
                for i in range(nr_of_items):
                    foodid = random.randint(1, 13)
                    order_items.append(foodid)
                    self.waiting = True
                dictToSend = {"items":order_items,"client_id":self.id_client}
                res = requests.post("http://" + str(self.host) + ":" + str(self.port) + "/order", json=dictToSend)
                print('response from server:', res.text)
                dictFromServer = res.json()

