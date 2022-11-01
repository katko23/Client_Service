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
        dict_orders = []
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
                dict_orders = dictFromServer['orders']
            while len(dict_orders) > 0:
                copy_d_o = dict_orders.copy()
                for o in copy_d_o:
                    # create a thread
                    thread = Thread(target=self.order_taking, args=(o, dict_orders))
                    # run the thread
                    thread.start()
                    # wait for the thread to finish
                    print('Waiting for the thread...')
                    thread.join()
            if(self.waiting == False) and len(Menu.menu) > 0:
                sum = 0
                for r in Setings.restaurant_rating:
                    sum = sum + r
                Setings.orders_nr = Setings.orders_nr + 1
                Setings.simulation_rating = (Setings.simulation_rating + sum / len(Setings.restaurant_rating))/Setings.orders_nr
                print(Setings.simulation_rating)

    def order_taking(self, o, dict_orders):
        address = o['restaurant_address']
        print("timesleep")
        time.sleep(o['estimated_waiting_time'] / 10)
        print("timego")
        res = requests.get(
            "http://" + str(address) + "/v" + str(o['restaurant_id']) + "/order" + "/" + str(o['order_id']))
        dict_r = res.json()
        print(o)
        if dict_r['cooking_time'] > 0:
            Setings.restaurant_rating[o['restaurant_id'] - 1] = raiting_time(o['registered_time'], time.time(), dict_r['max_wait'])
            d = raiting_time(0, dict_r['cooking_time'], dict_r['max_wait'])
            print(d)
            Setings.restaurant_rating[o['restaurant_id'] - 1] = d
            dict_orders.remove(o)
            self.waiting = False
        print("Response is ", res.text)


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

def raiting_time(time_i , time_s, max_wait):
    if (time_s - time_i) < max_wait : return 5
    elif max_wait <= (time_s - time_i) < max_wait * 1.1 : return 4
    elif max_wait * 1.1 <= (time_s - time_i) < max_wait * 1.2: return 3
    elif max_wait * 1.2 <= (time_s - time_i) < max_wait * 1.3:
        return 2
    elif max_wait * 1.3 <= (time_s - time_i) < max_wait * 1.4:
        return 1
    elif max_wait * 1.4 <= (time_s - time_i): return 0