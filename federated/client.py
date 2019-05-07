import random

class Client(object):
    def __init__(self, *args):
        pass
    def train(self):
        pass



class Server(object):
    def __init__(self, clients, model):
        self.clients = clients
        self.model = model
        
    def select_clients(self, possible_clients, num_clients):
        num_clients = min(num_clients, len(possible_clients))
        self.selected_clients = random.sample(possible_clients, num_clients)


    @property
    def online(self):
        return self.clients

    def train(self):
        pass




    
