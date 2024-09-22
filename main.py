import sys
import psycopg2
from datetime import date

# Database connection function
def create_connection():
    return psycopg2.connect(
        dbname='my_pet', 
        user='cindy',
        password='CODEWITHME', 
        host='localhost'
    )

# Helper function to execute queries
def execute_query(query, params=None, fetch=False):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall() if fetch else None

# Helper function to get user input with optional validation
def get_input(prompt, validation=None):
    value = input(prompt)
    return value if not validation else validation(value)

# Main menu options
def main_menu():
    options = [
        "Add Pet for Approval", "Approve Pet", "Reject Pet", 
        "Submit Adoption Request", "Approve Adoption", 
        "Reject Adoption", "View Pending Approvals", "Exit"
    ]
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    return get_input("Select an option: ")

# Add new pet for approval
def add_pet_for_approval():
    pet_data = [get_input(f"Enter pet's {field}: ") for field in ['name', 'species', 'breed']]
    execute_query(
        "INSERT INTO pets (name, species, breed, adoption_status, approval_status) VALUES (%s, %s, %s, 'available', 'pending')", 
        pet_data
    )
    print("Pet added for approval successfully.")

# Approve a pet
def approve_pet():
    pet_id = get_input("Enter the pet ID to approve: ", lambda x: int(x) if x.isdigit() else None)
    execute_query("UPDATE pets SET approval_status = 'approved' WHERE id = %s", (pet_id,))
    print(f"Pet with ID {pet_id} approved successfully.")

# Reject a pet
def reject_pet():
    pet_id = get_input("Enter the pet ID to reject: ", lambda x: int(x) if x.isdigit() else None)
    execute_query("DELETE FROM pets WHERE id = %s", (pet_id,))
    print(f"Pet with ID {pet_id} rejected and removed from the system.")

# Submit an adoption request
def submit_adoption_request():
    pet_id = get_input("Enter the pet ID for adoption: ", lambda x: int(x) if x.isdigit() else None)
    adopter_id = get_input("Enter adopter ID: ", lambda x: int(x) if x.isdigit() else None)
    
    # Check if the adopter exists
    if not execute_query("SELECT * FROM adopters WHERE id = %s", (adopter_id,), fetch=True):
        return print(f"No adopter found with ID {adopter_id}.")

    execute_query(
        "INSERT INTO adoptions (pet_id, adopter_id, adoption_date, status) VALUES (%s, %s, %s, 'pending')", 
        (pet_id, adopter_id, date.today())
    )
    print("Adoption request submitted successfully.")

# Approve an adoption request
def approve_adoption():
    adoption_id = get_input("Enter the adoption request ID to approve: ", lambda x: int(x) if x.isdigit() else None)
    execute_query("UPDATE adoptions SET status = 'approved' WHERE id = %s", (adoption_id,))
    print(f"Adoption request with ID {adoption_id} approved successfully.")

# Reject an adoption request
def reject_adoption():
    adoption_id = get_input("Enter the adoption request ID to reject: ", lambda x: int(x) if x.isdigit() else None)
    execute_query("UPDATE adoptions SET status = 'rejected' WHERE id = %s", (adoption_id,))
    print(f"Adoption request with ID {adoption_id} rejected successfully.")

# View pending approvals
def view_pending_approvals():
    pets = execute_query("SELECT * FROM pets WHERE approval_status = 'pending'", fetch=True)
    if pets:
        for pet in pets:
            print(f"ID: {pet[0]}, Name: {pet[1]}, Species: {pet[2]}, Breed: {pet[3]}, Status: {pet[4]}, Approval Status: {pet[5]}")
    else:
        print("No pets pending approval.")

# Main function
def main():
    actions = {
        '1': add_pet_for_approval,
        '2': approve_pet,
        '3': reject_pet,
        '4': submit_adoption_request,
        '5': approve_adoption,
        '6': reject_adoption,
        '7': view_pending_approvals,
        '8': sys.exit
    }
    
    while True:
        choice = main_menu()
        action = actions.get(choice)
        action() if action else print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
