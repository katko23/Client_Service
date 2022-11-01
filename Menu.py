import threading

menu_lock = threading.Lock()
menu = []
time_units = []
timeid = 0
clients_list = []
