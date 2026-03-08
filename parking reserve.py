import os
from datetime import datetime

# File name constant - stores all reservation data
FILE = "reservations.txt"

#  USER-DEFINED FUNCTIONS 

def create_file():
    # Check if file already exists before creating
    if not os.path.exists(FILE):
        f = open(FILE, 'w')
        # Write the column headers as the first line
        f.write("ReservationID|CustomerName|ReservationDate|SlotCode|PricePerUnit\n")
        f.close()


def make_reservation_id(name, date, slot):

    # String Operation: SLICING - get initials
    words = name.split()
    initials = ""
    for w in words:
        initials = initials + w[0]
    
    # String Operation: FORMATTING - convert date
    parts = date.split('/')
    day = parts[0]
    month = parts[1]
    year = parts[2]
    formatted_date = year + month + day
    
    # String Operation: CONCATENATION
    res_id = initials + "-" + formatted_date + "-" + slot
    
    return res_id


def save_reservation(res_id, name, date, slot, price):

    try:
        # File Operation: OPEN & WRITE
        f = open(FILE, 'a')
        
        # String Operation: CONCATENATION
        line = res_id + "|" + name + "|" + date + "|" + slot + "|" + str(price) + "\n"
        f.write(line)
        f.close()
        
        print("Data saved successfully!")
    
    except:
        # Handle any unexpected errors during file writing
        print("ERROR: Failed to save data!")
    
    finally:
        # This block always runs regardless of success or failure
        print("Save operation completed.")


def read_all_reservations():

    records = []
    
    try:
        # File Operation: OPEN & READ
        f = open(FILE, 'r')
        lines = f.readlines()
        f.close()
        
        # Process each line
        for line in lines[1:]: 
            # String Operation: SLICING
            line = line.strip()
            if line != "":
                parts = line.split('|')
                if len(parts) == 5:
                    records.append({
                        'id': parts[0], # Reservation ID
                        'name': parts[1], # Customer Name
                        'date': parts[2], # Reservation Date
                        'slot': parts[3], # Slot Code
                        'price': parts[4] # Price per Unit
                    })
    
    except FileNotFoundError:
        # Handle file not found error
        print("No reservations found.")
    
    finally:
        # This block always runs regardless of success or failure
        print("Read operation completed.")
    
    return records


def get_booked_slots(date):
    """
    Get list of booked slots for a specific date
    String Operation: SEARCHING
    """
    records = read_all_reservations()
    booked = []
    
    # String Operation: SEARCHING
    for r in records:
        if r['date'] == date:
            booked.append(r['slot'])
    
    return booked


def get_available_slots(category_code, max_slots, date):
    """
    Get list of available slots for category and date
    """
    booked = get_booked_slots(date)
    available = []
    
    # Create all slots
    for i in range(1, max_slots + 1):
        # String Operation: FORMATTING
        if i < 10:
            slot_code = category_code + "0" + str(i)
        else:
            slot_code = category_code + str(i)
        
        # Check if not booked
        slot_booked = ""
        for b in booked:
            if b == slot_code:
                slot_booked = "YES"
        
        if slot_booked == "":
            available.append(slot_code)
    
    return available


def search_by_id(search_id):
    """
    Search reservation by ID
    String Operation: SEARCHING
    """
    records = read_all_reservations()
    found = ""
    
    # String Operation: SEARCHING
    for r in records:
        if r['id'] == search_id:
            found = r
    
    return found


def count_by_date(target_date):
    """
    Count reservations for specific date
    """
    records = read_all_reservations()
    count = 0
    matches = []
    
    for r in records:
        if r['date'] == target_date:
            count = count + 1
            matches.append(r)
    
    return count, matches


def count_by_category():
    """
    Count reservations by parking category
    String Operation: SEARCHING
    """
    records = read_all_reservations()
    
    rc_count = 0
    mc_count = 0
    vip_count = 0
    dp_count = 0
    ev_count = 0
    
    # String Operation: SEARCHING
    for r in records:
        slot = r['slot']
        
        if slot[0:2] == "RC":
            rc_count = rc_count + 1
        
        if slot[0:2] == "MC":
            mc_count = mc_count + 1
        
        if slot[0:3] == "VIP":
            vip_count = vip_count + 1
        
        if slot[0:2] == "DP":
            dp_count = dp_count + 1
        
        if slot[0:2] == "EV":
            ev_count = ev_count + 1
    
    return rc_count, mc_count, vip_count, dp_count, ev_count


#  MAIN PROGRAM 

print("="*60)
print("PARKING SLOT RESERVATION SYSTEM")
print("="*60)
print("Kolej Profesional MARA Indera Mahkota")
print("="*60)

# Create file
create_file()
print("System ready!")

# Main loop
exit_program = ""

for i in range(100):
    
    if exit_program == "YES":
        break
    
    # Display menu
    print("\n" + "="*60)
    print("MAIN MENU")
    print("="*60)
    print("1. Make New Reservation")
    print("2. Search Reservation by ID")
    print("3. Count Reservations by Date")
    print("4. Count Reservations by Category")
    print("5. View All Reservations")
    print("6. Exit")
    print("="*60)
    
    choice = input("Enter your choice (1-6): ")
    
    # OPTION 1: MAKE NEW RESERVATION
    if choice == "1":
        print("\n" + "="*60)
        print("NEW RESERVATION")
        print("="*60)
        
        # Get customer name
        customer_name = ""
        while customer_name == "":
            name_input = input("\nEnter Customer Name (UPPERCASE): ").strip()
            
            # String Operation: MODIFYING
            if name_input.isupper() and name_input != "":
                customer_name = name_input
                print(f"Name accepted: {customer_name}")
            else:
                print("ERROR: Customer name must be in UPPERCASE!")
                print("Please re-enter.")
        
        # Get reservation date
        reservation_date = ""
        while reservation_date == "":
            date_input = input("\nEnter Reservation Date (DD/MM/YYYY): ").strip()
            
            # Exception Handling: try-except-finally
            try:
                # Validate date
                date_obj = datetime.strptime(date_input, "%d/%m/%Y")
                
                # Check past date
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                if date_obj < today:
                    print("ERROR: Cannot book past dates!")
                else:
                    reservation_date = date_input
                    print(f"Date accepted: {reservation_date}")
            
            except ValueError:
                print("ERROR: Invalid date format!")
                print("Please use DD/MM/YYYY format")
            
            finally:
                print("Date validation completed.")
        
        # Select category
        print("\n" + "-"*60)
        print("PARKING CATEGORIES")
        print("-"*60)
        print("1. Regular Car Parking (RC) - RM5.00 per hour")
        print("2. Motorcycle Parking (MC) - RM2.00 per hour")
        print("3. VIP Parking (VIP) - RM15.00 per hour")
        print("4. Disabled Parking (DP) - RM3.00 per hour")
        print("5. EV Charging Parking (EV) - RM10.00 per hour")
        print("-"*60)
        
        category_code = ""
        price = 0
        max_slots = 0
        category_name = ""
        
        # Loop until valid category is selected
        while category_code == "":
            category_input = input("\nSelect category (1-5): ")
            
            if category_input == "1":
                category_code = "RC"
                price = 5.00
                max_slots = 20
                category_name = "Regular Car Parking"
            
            if category_input == "2":
                category_code = "MC"
                price = 2.00
                max_slots = 30
                category_name = "Motorcycle Parking"
            
            if category_input == "3":
                category_code = "VIP"
                price = 15.00
                max_slots = 5
                category_name = "VIP Parking"
            
            if category_input == "4":
                category_code = "DP"
                price = 3.00
                max_slots = 5
                category_name = "Disabled Parking"
            
            if category_input == "5":
                category_code = "EV"
                price = 10.00
                max_slots = 10
                category_name = "EV Charging Parking"
            
            if category_code == "":
                print("ERROR: Invalid category selection!")
                print("Please choose 1-5")
            else:
                print(f"Selected: {category_name}")
        
        # Get available slots
        print("\n" + "-"*60)
        print("AVAILABLE SLOTS")
        print("-"*60)
        
        available_slots = get_available_slots(category_code, max_slots, reservation_date)
        
        # Check if slots available
        if len(available_slots) == 0:
            print("Sorry! No available slots for this date.")
            print("Please choose different date or category.")
            continue
        
        # Display available slots
        for j in range(0, len(available_slots), 5):
            print(" ".join(available_slots[j:j+5]))
        
        print("-"*60)
        
        # Get slot selection
        selected_slot = ""
        while selected_slot == "":
            slot_input = input(f"\nEnter Slot Code (e.g., {available_slots[0]}): ").strip().upper()
            
            # Check if valid
            slot_valid = ""
            for s in available_slots:
                if s == slot_input:
                    slot_valid = "YES"
            
            if slot_valid == "YES":
                selected_slot = slot_input
                print(f"Slot selected: {selected_slot}")
            else:
                print("ERROR: Invalid or unavailable slot!")
                print("Please choose from available slots above.")
        
        # Generate ID
        print("\n" + "-"*60)
        print("GENERATING RESERVATION ID")
        print("-"*60)
        reservation_id = make_reservation_id(customer_name, reservation_date, selected_slot)
        print(f"Reservation ID: {reservation_id}")
        
        # Save reservation
        print("\n" + "-"*60)
        print("SAVING RESERVATION")
        print("-"*60)
        
        save_reservation(reservation_id, customer_name, reservation_date, selected_slot, price)
        
        # Display confirmation
        print("\n" + "="*60)
        print("RESERVATION SUCCESSFUL!")
        print("="*60)
        print(f"Reservation ID  : {reservation_id}")
        print(f"Customer Name   : {customer_name}")
        print(f"Reservation Date: {reservation_date}")
        print(f"Category        : {category_name}")
        print(f"Slot Code       : {selected_slot}")
        print(f"Price per Unit  : RM{price:.2f}")
        print("="*60)
        print("Thank you for your reservation!")
    
    # OPTION 2: SEARCH RESERVATION
    if choice == "2":
        print("\n" + "="*60)
        print("SEARCH RESERVATION BY ID")
        print("="*60)
        
        # Get ID from user
        search_id = input("\nEnter Reservation ID: ").strip().upper()
        
        # Check if ID is empty
        if search_id == "":
            print("ERROR: Reservation ID cannot be empty!")
        else:
            print("\nSearching...")
            result = search_by_id(search_id)
            
            if result != "":
                # Display found
                print("\n" + "="*60)
                print("RESERVATION FOUND")
                print("="*60)
                print(f"Reservation ID  : {result['id']}")
                print(f"Customer Name   : {result['name']}")
                print(f"Reservation Date: {result['date']}")
                print(f"Slot Code       : {result['slot']}")
                print(f"Price per Unit  : RM{result['price']}")
                print("="*60)
            else:
                # Display not found
                print("\n" + "="*60)
                print("RESERVATION NOT FOUND")
                print("="*60)
                print(f"No reservation exists with ID: {search_id}")
                print("\nPossible reasons:")
                print("- The Reservation ID may be incorrect")
                print("- The reservation may not exist")
                print("="*60)
    
    # OPTION 3: COUNT BY DATE
    if choice == "3":
        print("\n" + "="*60)
        print("COUNT RESERVATIONS BY DATE")
        print("="*60)
        
        # Get date from user
        target_date = input("\nEnter Date (DD/MM/YYYY): ").strip()
        
        # Check if date is empty
        if target_date == "":
            print("ERROR: Date cannot be empty!")
        else:
            print("\nCounting...")
            count, matches = count_by_date(target_date)
            
            print("\n" + "="*60)
            print(f"RESERVATIONS FOR {target_date}")
            print("="*60)
            print(f"Total Bookings: {count}")
            
            if count > 0:
                print("\nDetails:")
                print("-"*60)
                for i in range(len(matches)):
                    m = matches[i]
                    print(f"{i+1}. ID: {m['id']}")
                    print(f"   Customer: {m['name']}")
                    print(f"   Slot: {m['slot']}")
                    print("-"*60)
            else:
                print("\nNo reservations found for this date.")
            
            print("="*60)
    
    # OPTION 4: COUNT BY CATEGORY
    if choice == "4":
        print("\n" + "="*60)
        print("COUNT RESERVATIONS BY CATEGORY")
        print("="*60)
        
        print("\nCalculating...")
        rc, mc, vip, dp, ev = count_by_category()
        total = rc + mc + vip + dp + ev
        
        print("\n" + "="*60)
        print("BOOKING STATISTICS BY CATEGORY")
        print("="*60)
        print(f"Regular Car Parking  : {rc} booking(s)")
        print(f"Motorcycle Parking   : {mc} booking(s)")
        print(f"VIP Parking          : {vip} booking(s)")
        print(f"Disabled Parking     : {dp} booking(s)")
        print(f"EV Charging Parking  : {ev} booking(s)")
        print("-"*60)
        print(f"TOTAL                : {total} booking(s)")
        print("="*60)
    
    # OPTION 5: VIEW ALL
    if choice == "5":
        print("\n" + "="*60)
        print("ALL RESERVATIONS")
        print("="*60)
        
        # Read all reservations
        records = read_all_reservations()
        
        # Check if no reservations found
        if len(records) == 0:
            print("\nNo reservations found.")
        else:
            print(f"\n{'No.':<4} {'Reservation ID':<20} {'Name':<20} {'Date':<12} {'Slot':<8} {'Price':<8}")
            print("-"*80)
            
            for i in range(len(records)):
                r = records[i]
                print(f"{i+1:<4} {r['id']:<20} {r['name']:<20} {r['date']:<12} {r['slot']:<8} RM{r['price']:<6}")
            
            print("-"*80)
            print(f"Total: {len(records)}")
        
        print("="*60)
    
    # OPTION 6: EXIT
    if choice == "6":
        print("\n" + "="*60)
        print("EXITING SYSTEM")
        print("="*60)
        print(""*60)
        print("Thank you for using the system!")
        print(""*60)
        print("="*60)
        exit_program = "YES"
    
    # Invalid choice
    if choice not in ["1", "2", "3", "4", "5", "6"]:
        print("\n" + "="*60)
        print("ERROR: INVALID CHOICE")
        print("="*60)
        print(f"You entered: {choice}")
        print("Please choose 1-6")
        print("="*60)

# Program end
print("\nProgram ended successfully.")
print("Data saved to:", FILE)
print()