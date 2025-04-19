
class Client:
    def __init__(self, id, name, status="active"):
        self.id = id
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }
