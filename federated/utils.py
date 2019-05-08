from federated import ClientModel

def setup_clients(num):
    return [ClientModel() for _ in range(num)]
