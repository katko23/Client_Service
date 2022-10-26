import random
from threading import Thread
import Setings
import threading
import time,math
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
        import Menu
        while True:
            if self.waiting == False and len(Menu.menu) > 0:
                dict_S = []
                for r in Menu.menu:
                    nr_of_items = random.randint(1, 4)
                    order_items = []
                    dict_order = {}
                    for i in range(nr_of_items):
                        foodid = random.randint(1, r['nr_of_items']-1)
                        order_items.append(foodid)
                        self.waiting = True
                    dict_order['restaurant_id'] = r['restaurant_id']
                    dict_order['items'] = order_items
                    dict_order['priority'] = 3
                    dict_order['max_wait'] = math.ceil(self.maxTime(order_items))
                    dict_order['created_time'] = time.time()
                    dict_S.append(dict_order)
                dictToSend = {"client_id": self.id_client, "orders":dict_S}
                res = requests.post("http://" + str(self.host) + ":" + str(self.port) + "/order", json=dictToSend)
                print('response from server:', res.text)
                dictFromServer = res.json()

    def maxTime(self, items):
        import Menu
        max = 0
        for i in items:
            for r in Menu.menu:
                for f in r['menu']:
                    if i == f['id']:
                        if max < f['preparation-time']:
                            max = f['preparation-time']

        max = max * 1.8;
        return max