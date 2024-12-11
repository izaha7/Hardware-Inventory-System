from models.CPA import CPA
from models.Client import Client
from models.TaxReturn import TaxReturn
from models.Assistant import Assistant
from connection import create_connection
import database

MENU_PROMPT = """Tax Return System

1) Add a CPA
2) Add a Tax Filing Assistant
3) Add a Client
4) Add a tax return for a client
5) Mark a clients materials as provided
6) Check a clients materials status
7) Mark a clients tax return as filed
8) Check a clients tax return status
9) Mark tax return as checked by CPA
10) Check if tax return was checked by CPA
11) Exit

Enter your choice: """

# A series of prompt functions to help guide the user through the options

def prompt_add_cpa():
    name = input("Insert CPA name: ")
    email = input("Insert CPA email: ")
    cpa = CPA(name, email)
    cpa.save()
    print(f"CPA with the name {name} has been added.")

def prompt_add_assistant():
    name = input("Insert Assistant name: ")
    email = input("Insert Assistant email: ")
    assistant = Assistant(name, email)
    assistant.save()
    print(f"Assistant {name} added successfully.")

def prompt_add_client():
    name = input("Insert client name: ")
    address = input("Insert client address: ")
    income = float(input("Insert client income: "))
    cpa_id = int(input("Insert the ID for the CPA for this client: "))
    client = Client(name, address, income, cpa_id)
    client.save()
    print(f"{name} added successfully.")

def prompt_add_tax_return():
    client_id = int(input("Insert the client ID for this tax return: "))
    tax_return = TaxReturn(client_id)
    tax_return.save()
    print(f"Tax return for client {client_id} has been added.")

def prompt_mark_materials_provided():
    client_id = int(input("Insert client ID: "))
    client = Client.get(client_id)
    if client:
        client.mark_materials()
        print(f"Materials for client {client_id} marked as provided.")
    else:
        print("Client not found.")

def prompt_check_materials_status():
    client_id = int(input("Insert client ID: "))
    client = Client.get(client_id)
    if client.materials_provided:
        print("The materials for this client have been provided.")
    else:
        print("The materials for this client have not been provided.")

def prompt_mark_filed():
    return_id = int(input("Insert tax return ID: "))
    tax_return = TaxReturn.get(return_id)
    if tax_return:
        tax_return.mark_filed()
        print(f"Tax return with ID {return_id} is now marked as filed.")
    else:
        print(f"Tax return with ID {return_id} does not exist.")


def prompt_check_return():
   return_id = int(input("Insert tax return ID: "))
   tax_return = TaxReturn.get(return_id)
   if tax_return:
        print(f"Tax return status: {tax_return.status}")
   else:
       print("Tax return not found.")


def prompt_mark_cpa_checked():
    return_id = int(input("Insert tax return ID: "))
    tax_return = TaxReturn.get(return_id)
    if tax_return:
        tax_return.mark_cpa_checked()
        print(f"Tax return {return_id} marked as checked by CPA.")
    else:
        print("Tax return not found.")


def prompt_check_cpa_checked():
    return_id = int(input("Insert tax return ID: "))
    tax_return = TaxReturn.get(return_id)

    if tax_return:
        checked = tax_return.cpa_checked
        print(f"CPA checked: {'Yes' if checked else 'No'}")
    else:
        print(f"Tax return with ID {return_id} does not exist.")

MENU_OPTIONS = {
    "1": prompt_add_cpa,
    "2": prompt_add_assistant,
    "3": prompt_add_client,
    "4": prompt_add_tax_return,
    "5": prompt_mark_materials_provided,
    "6": prompt_check_materials_status,
    "7": prompt_mark_filed,
    "8": prompt_check_return,
    "9": prompt_mark_cpa_checked,
    "10": prompt_check_cpa_checked
}

def menu():
    connection = create_connection()
    database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "11":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Enter a valid input")

if __name__ == "__main__":
    menu()
