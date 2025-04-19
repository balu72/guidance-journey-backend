
class Document:
    def __init__(self, id, client_id, name):
        self.id = id
        self.client_id = client_id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "name": self.name
        }
