import random


class Client(object):
    def __init__(self, client_id, model, train_data, test_data):
        self.id = client_id
        self.model = model
        self.train_data = train_data
        self.test_data = test_data

    # TODO: Finish this method
    def train(self, epochs, batch_size):
        for i in range(epochs):
            update = self.model.train(train_data)
        num_train_samples = len(self.train_data)
        return num_train_samples, update



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
