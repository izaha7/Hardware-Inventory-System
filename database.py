from typing import Tuple
from connection import create_connection
# type hinting
CPA = Tuple[int, str, str]
Client = Tuple[int, str, str, float, bool, int]
TaxReturn = Tuple[int, int, str, bool, str]
Assistant = Tuple[int, str, str]
# Create table queries, some of which having default values
CREATE_CPA = """CREATE TABLE IF NOT EXISTS cpa
(id SERIAL PRIMARY KEY, name TEXT, email TEXT UNIQUE);"""
CREATE_ASSISTANT = """CREATE TABLE IF NOT EXISTS assistants
(id SERIAL PRIMARY KEY, name TEXT, email TEXT UNIQUE);"""
CREATE_CLIENTS = """CREATE TABLE IF NOT EXISTS clients
(id SERIAL PRIMARY KEY, name TEXT, address TEXT, income DECIMAL, materials_provided BOOLEAN DEFAULT FALSE, cpa_id INTEGER REFERENCES cpa(id));"""
CREATE_TAX_RETURN = """CREATE TABLE IF NOT EXISTS tax_returns
(id SERIAL PRIMARY KEY, client_id INTEGER REFERENCES clients(id) UNIQUE, status TEXT DEFAULT 'Needs filing', cpa_checked BOOLEAN DEFAULT FALSE, filed_timestamp TIMESTAMP);"""
#Queries to insert into tables
INSERT_CPA = "INSERT INTO cpa (name, email) VALUES (%s, %s) RETURNING id;"
INSERT_ASSISTANT = "INSERT INTO assistants (name, email) VALUES (%s, %s) RETURNING id;"
INSERT_CLIENT = "INSERT INTO clients (name, address, income, cpa_id) VALUES (%s, %s, %s, %s) RETURNING id;"
INSERT_TAX_RETURN = "INSERT INTO tax_returns (client_id) VALUES (%s) RETURNING id;"
#Queries to select from tables
SELECT_CPA = "SELECT * FROM cpa WHERE id = %s;"
SELECT_ASSISTANT = "SELECT * FROM assistants WHERE id = %s;"
SELECT_CLIENT = "SELECT * FROM clients WHERE id = %s;"
SELECT_TAX_RETURN = "SELECT * FROM tax_returns WHERE id = %s;"
#Queries to update tables
UPDATE_MATERIALS = "UPDATE clients SET materials_provided = %s WHERE id = %s;"
UPDATE_TAX_RETURN = "UPDATE tax_returns SET status = %s, filed_timestamp = %s WHERE id = %s;"
UPDATE_CPA_CHECKED_TAX_RETURN = "UPDATE tax_returns SET cpa_checked = %s WHERE id = %s;"
#Creates all the tables by calling the creation queries
def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CPA)
            cursor.execute(CREATE_ASSISTANT)
            cursor.execute(CREATE_CLIENTS)
            cursor.execute(CREATE_TAX_RETURN)

#Following functions create objects for whatever the user selects
def create_cpa(name: str, email: str):
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CPA, (name, email))
            return cursor.fetchone()[0]


def create_assistant(connection, name: str, email: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ASSISTANT, (name, email))
            return cursor.fetchone()[0]

def create_client(connection, name: str, address: str, income: float, cpa_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CLIENT, (name, address, income, cpa_id))
            return cursor.fetchone()[0]

def create_tax_return(connection, client_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_TAX_RETURN, (client_id,))
            return cursor.fetchone()[0]

def get_cpa(connection, cpa_id: int) -> CPA:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CPA, (cpa_id,))
            return cursor.fetchone()

def get_assistant(connection, assistant_id: int) -> Assistant:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ASSISTANT, (assistant_id,))
            return cursor.fetchone()

def get_client(connection, client_id: int) -> Client:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CLIENT, (client_id,))
            return cursor.fetchone()


def get_tax_return(connection, return_id: int) -> TaxReturn:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_TAX_RETURN, (return_id,))
            tax_return_data = cursor.fetchone()
            return tax_return_data

#The following functions call the update queries as selected by the user
def update_materials_status(connection, client_id: int, status: bool):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_MATERIALS, (status, client_id))

def update_tax_return_status(connection, return_id: int, status: str, timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_TAX_RETURN, (status, timestamp, return_id))


def cpa_checked(connection, return_id: int, checked: bool):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CPA_CHECKED_TAX_RETURN, (checked, return_id))
