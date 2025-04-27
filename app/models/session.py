
class Session:
    def __init__(self, id, client_id, date, completed=False):
        self.id = id
        self.client_id = client_id
        self.date = date
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "date": self.date,
            "completed": self.completed
        }
