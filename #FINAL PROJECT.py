#FINAL PROJECT
#PROJECT TITLE: PARKING SLOT RESERVATION SYSTEM
#AUTHOR: IRFAN

import os
from datetime import datetime

RESERVATION_FILE = "reservations.txt"

CATEGORIES = {
    "1": {"name": "Regular Car", "code": "RC", "price": 5.00, "slots": 20},
    "2": {"name": "Motorcycle", "code": "MC", "price": 2.00, "slots": 30},
    "3": {"name": "VIP", "code": "VIP", "price": 15.00, "slots": 5},
    "4": {"name": "Disabled", "code": "DP", "price": 3.00, "slots": 5},
    "5": {"name": "EV Charging", "code": "EV", "price": 10.00, "slots": 10}
}

def create_file():
    """
    USER-DEFINED FUNCTION
    Create reservation file if it doesn't exist
    File Operation: CREATE FILE
    """
    if not os.path.exists(RESERVATION_FILE):
        file = open(RESERVATION_FILE, 'w')
        file.write("ReservationID|CustomerName|ReservationDate|SlotCode|PricePerUnit\n")
        file.close()
        print("File created successfully!")


def get_name():
    """
    USER-DEFINED FUNCTION
    Get customer name in UPPERCASE
    String Operation: MODIFYING (isupper check)
    """
    name = input("\nEnter Customer Name (UPPERCASE): ").strip()
    
    # String Operation: MODIFYING - check if uppercase
    if name.isupper() and name != "":
        return name
    else:
        print("ERROR: Name must be in UPPERCASE!")
        return None
    
