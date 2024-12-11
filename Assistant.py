import database
from connection import create_connection

class Assistant:
    def __init__(self, name: str, email: str, _id: int = None):
        self.id = _id
        self.name = name
        self.email = email

    # updates the ID with the ID that is returned (saves the assistant)
    def save(self):
        connection = create_connection()
        self.id = database.create_assistant(connection, self.name, self.email)
        connection.close()

    # Gets the assistant data and creates an instance
    @classmethod
    def get(cls, assistant_id: int) -> "Assistant":
        connection = create_connection()
        assistant_data = database.get_assistant(connection, assistant_id)
        connection.close()
        if assistant_data:
            return cls(assistant_data[1], assistant_data[2], assistant_data[0])

