import database
from connection import create_connection

class Client:
    def __init__(self, name: str, address: str, income: float, cpa_id: int, materials_provided: bool = False, _id: int = None):
        self.id = _id
        self.name = name
        self.address = address
        self.income = income
        self.materials_provided = materials_provided
        self.cpa_id = cpa_id

    # updates the client ID with what is returned by the database
    def save(self):
        connection = create_connection()
        new_client_id = database.create_client(connection, self.name, self.address, self.income, self.cpa_id)
        connection.close()
        self.id = new_client_id

    # gets client data
    @classmethod
    def get(cls, client_id: int) -> "Client":
        connection = create_connection()
        client_data = database.get_client(connection, client_id)
        connection.close()
        return cls(client_data[1], client_data[2], client_data[3], client_data[5], client_data[4], client_data[0])

    # indicates that a client has provided tax materials
    def mark_materials(self):
        self.materials_provided = True
        connection = create_connection()
        database.update_materials_status(connection, self.id, self.materials_provided)
        connection.close()
