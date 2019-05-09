import random
import torch
import torch.optim as optim


class Client(object):
    def __init__(self, client_id: int, model: ComputationModel, train_loader, test_loader):
        self.id = client_id
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader

    def train_model(self, epochs, batch_size):
        """  
        return:
            (num_train_samples, update)
                num_train_samples:                  int
                update:     model.parameters()      [Tensor]
        """
        for i in range(epochs):
            update = self._train(self.train_loader)
        num_train_samples = len(self.train_loader.dataset)
        return num_train_samples, update

    def _train(self, train_loader):
        """
        returns:
            update: [Tensor] 
        """
        local_model = self.model.clone()
        local_parameters_generator = local_model.train(self.train_loader)
        update = []
        for local_param, init_param in \
                enumerate(zip(local_parameters_generator, self.model.parameters())):
            update.append(local_model-init_param)
        return update


class Server(object):
    def __init__(self, clients, model):
        self.clients = clients
        self.model = model
        self.updates = []
        self.selected_clients = []

    def select_clients(self, possible_clients, num_clients):
        num_clients = min(num_clients, len(possible_clients))
        self.selected_clients = random.sample(possible_clients, num_clients)

    @property
    def online(self):
        return self.clients

    def send_to_clients(self):
        for client in self.select_clients:
            client.model = self.model

    ####
    #   updates = server.train_model()
    #   server.update_model(updates)
    #   server.send_to_clients()
    #
    def train_model(self):
        self.updates = []
        clients = self.selected_clients
        for client in clients:
            update = client.train_model()
            self.updates.append(update)

    def update_model(self):
        """
        Args:
            updates:    [(num_train_samples, update), ...]
                update:     [Tensor]
        """
        total_samples = 0
        final_update = [0 for _ in self.model.model.parameters()]
        for num_train_samples, update in updates:
            total_samples += num_train_samples
            for i, param in enumerate(update):
                final_update[i] += param * num_train_samples
        for i, update in final_update:
            final_update[i] /= total_samples
        self.model.update(final_update)


# class ServerModel(object):
#     def __init__(self, model):
#         self.model = model

#     def update(self, updates):
#         """
#         Args:
#             updates: [(num_train_samples, update), ...]
#         """
#         total_samples = 0
#         final_update = 0
#         for num_train_samples, update in updates:
#             total_samples += num_train_samples
#             final_update = num_train_samples*update
#         final_update /= total_samples
#         self.model.update(final_update)


# class ClientModel(object):
#     def __init__(self, *args, **kwargs):
#         return super().__init__(*args, **kwargs)

#     def train(self):
#         update = 0
#         return update


class ComputationModel(object):
    def __init__(self, model, lr, loss_func):
        self.model = model
        self.lr = lr
        self.loss_func = loss_func
        self.optimizer = optim.SGD(model.parameters(), lr=self.lr)

    def clone(self):
        return ComputationModel(self.model.clone(), lr, loss_func)

    def train(self, train_loader):
        """
            Returns:
                model.parameters():     generator<Tensor>
        """
        for data, target in train_loader:
            output = self.model(data)
            self.optimizer.zero_grad()
            loss = self.loss_func(output, target)
            loss.backward()
            self.optimizer.step()
        return self.model.parameters()

    def test(self):
        pass

    def update(self, update):
        """
        Args:
            update:     [Tensor]
        """
        for i, param in enumerate(self.model.parameters()):
            param.data = update[i]
