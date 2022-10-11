from Lab1.Client_Service import ClientServer, TownChisinau

municipiu = TownChisinau.Chisinau()

if __name__ == "__main__":
    server = ClientServer.Server()
    server.start()

    # municipiu = TownChisinau.Chisinau()
    municipiu.start()