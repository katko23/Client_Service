from threading import Thread
import threading
from flask import Flask, render_template, request, url_for, jsonify
import TownChisinau
import Setings

hostName = Setings.serverName
serverPort = Setings.this_serverPort

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = Flask(__name__)

        @app.route('/client', methods=['POST'])
        def client_endpoint():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from Ordering Service:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            id = input_json['client_id']
            import ClientServiceMain


            ClientServiceMain.municipiu.clients[id].waiting = False
            serverLock.release()
            print("Order is ", input_json)
            dictToReturn = {'answer': "Client received"}
            return jsonify(dictToReturn)

        @app.route('/menu', methods=['GET'])
        def client_menu_endpoint():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('Menu get from Server:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            tempr = input_json['restaurants_data']
            import Menu
            for r in tempr:
                dict = { 'restaurant_id':r['restaurant_id'], 'menu':r['menu'] , 'nr_of_items':r['menu_items']}
                Menu.menu.append(dict);

            serverLock.release()
            print("Menu is ", Menu.menu)
            dictToReturn = {'Answer': "Client received"}
            return jsonify(dictToReturn)

        app.run(host=hostName, port=serverPort, debug=False)