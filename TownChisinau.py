import ClientThread
import Setings

class Chisinau:
    clients = []*Setings.max_nr_of_clients

    def start(self):
        for i in range(Setings.max_nr_of_clients):
            tempclient = ClientThread.Client(i)
            tempclient.start()
            self.clients.append(tempclient)