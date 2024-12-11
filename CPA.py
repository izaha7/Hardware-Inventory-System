import database

class CPA:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.id = None

    # updates the id with what is returned by the database
    def save(self):
        self.id = database.create_cpa(self.name, self.email)

    # gets cpa data
    @staticmethod
    def get(cpa_id: int):
        cpa_data = database.get_cpa(cpa_id)
        if cpa_data:
            cpa = CPA(cpa_data[1], cpa_data[2])
            cpa.id = cpa_data[0]
            return cpa

