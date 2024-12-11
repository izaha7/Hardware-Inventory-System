from datetime import datetime
import database
from connection import create_connection


class TaxReturn:
    def __init__(self, client_id: int, _id: int = None, status: str = None, cpa_checked: bool = False, filed_timestamp: str = None):
        self.id = _id
        self.client_id = client_id
        self.status = status
        self.cpa_checked = cpa_checked
        self.filed_timestamp = filed_timestamp

    # inserts the tax return into the database, updating an ID if given by the user
    def save(self):
        if self.id is None:
            connection = create_connection()
            self.id = database.create_tax_return(connection, self.client_id) #self.status, self.filed_timestamp)
            connection.close()
        else:
            print("A tax return already exists for this ID")

    # gets tax return data, printing back the timestamp
    @classmethod
    def get(cls, return_id: int) -> "TaxReturn":
        connection = create_connection()
        tax_return = database.get_tax_return(connection, return_id)
        if not tax_return:
            raise ValueError(f"Tax return with ID {return_id} does not exist.")
        print(f"Tax return timestamp: {tax_return[4]}")
        return cls(tax_return[1], tax_return[0], tax_return[2], tax_return[3])

    # update the status of a tax return in the database to "filed" and record the timestamp of when it was filed
    def mark_filed(self):
        self.status = "Filed"
        timestamp = datetime.now()
        connection = create_connection()
        database.update_tax_return_status(connection, self.id, self.status, timestamp)
        connection.close()

    # updates the database to show that the CPA was checked
    def mark_cpa_checked(self):
        self.cpa_checked = True
        connection = create_connection()
        database.cpa_checked(connection, self.id, self.cpa_checked)
        connection.close()

