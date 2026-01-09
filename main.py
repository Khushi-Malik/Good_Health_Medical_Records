"""
Medicine Inventory Management System
A simple CLI application to manage medical store inventory.
"""

import pickle
import os
import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class MedicineType(Enum):
    """Enum for medicine types"""
    SYRUP = 0
    TABLET = 1


class Medicine:
    """Class to represent a medicine"""
    def __init__(self, m_id: int, name: str, brand: str, 
                 man_date: str, exp_date: str, m_type: int, 
                 quantity: int, price: float):
        self.id = m_id
        self.name = name
        self.brand = brand
        self.manufacturing_date = man_date
        self.expiry_date = exp_date
        self.type = m_type
        self.quantity = quantity
        self.price = price
        self.amount = quantity * price
    
    def to_list(self) -> List[Any]:
        """Convert medicine object to list format for backward compatibility"""
        return [self.id, self.name, self.brand, self.manufacturing_date, 
                self.expiry_date, self.type, self.quantity, self.price, self.amount]
    
    @classmethod
    def from_list(cls, data: List[Any]) -> 'Medicine':
        """Create medicine object from list format"""
        return cls(data[0], data[1], data[2], data[3], data[4], 
                   data[5], data[6], data[7])


def clear_screen() -> None:
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu() -> None:
    """Display the instructions and features of the program"""
    clear_screen()
    print("=" * 75)
    print("  GOOD HEALTH FAMILY MEDICAL STORE - INVENTORY MANAGEMENT SYSTEM  ".center(75))
    print("=" * 75)
    print("\n")
    print("\t\t\t 1. ADD STOCK")
    print("\t\t\t 2. UPDATE STOCK")
    print("\t\t\t 3. DELETE MEDICINE")
    print("\t\t\t 4. SELL MEDICINE")
    print("\t\t\t 5. RETURN MEDICINE")
    print("\t\t\t 6. UPCOMING EXPIRY MEDICINE LIST")
    print("\t\t\t 7. SEARCH MEDICINE")
    print("\t\t\t 8. VIEW ALL MEDICINES")
    print("\t\t\t 0. EXIT")
    print("\n")
    print("=" * 75)


def medicine_expired(date: datetime.date) -> bool:
    """Check if the medicine has expired"""
    return date <= datetime.date.today()


def check_valid_date(date_str: str) -> bool:
    """Check if an input date string is valid"""
    try:
        date = datetime.datetime.strptime(date_str, "%Y, %m, %d")
        # Check if date is not in the future for manufacturing date
        return True
    except ValueError:
        return False


def parse_date(date_str: str) -> datetime.date:
    """Parse date string to date object"""
    return datetime.datetime.strptime(date_str, "%Y, %m, %d").date()


def load_medicines() -> List[List[Any]]:
    """Load medicines from file"""
    if os.path.exists('Medicines.dat'):
        try:
            with open("Medicines.dat", "rb") as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError):
            print("\n\t\t ## ERROR READING FILE. Starting with empty database ##")
            return []
    return []


def save_medicines(medicines: List[List[Any]]) -> bool:
    """Save medicines to file"""
    try:
        with open("Medicines.dat", "wb") as f:
            pickle.dump(medicines, f)
        return True
    except Exception as e:
        print(f"\n\t\t ## ERROR SAVING FILE: {e} ##")
        return False


def get_medicine_type_name(m_type: int) -> str:
    """Get readable name for medicine type"""
    return "Tablet" if m_type == 1 else "Syrup"


def add_stock() -> None:
    """Add medicines to the database"""
    medicines = load_medicines()
    
    # Generate new ID
    m_id = max([med[0] for med in medicines], default=0) + 1
    
    print('\n\n\t\t\t Medicine ID: ', m_id)
    m_name = input('\n\t\t\t Enter Medicine Name: ').strip()
    if not m_name:
        print("\n\t\t\t ## MEDICINE NAME CANNOT BE EMPTY ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return
    
    m_brand = input('\n\t\t\t Enter Medicine Brand Name: ').strip()

    # Manufacturing Date
    man_date = input('\n\t\t\t Enter Medicine Manufacturing Date (yyyy, mm, dd): ')
    while not check_valid_date(man_date):
        print("\t\t\t ## INVALID DATE FORMAT ##")
        man_date = input('\n\t\t\t Enter Medicine Manufacturing Date (yyyy, mm, dd): ')
    
    # Expiry Date
    exp_date = input('\n\t\t\t Enter Medicine Expiry Date (yyyy, mm, dd): ')
    while not check_valid_date(exp_date):
        print("\t\t\t ## INVALID DATE FORMAT ##")
        exp_date = input('\n\t\t\t Enter Medicine Expiry Date (yyyy, mm, dd): ')
    
    # Validate expiry date is after manufacturing date
    if parse_date(exp_date) <= parse_date(man_date):
        print("\n\t\t\t ## EXPIRY DATE MUST BE AFTER MANUFACTURING DATE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return
    
    # Check if already expired
    if parse_date(exp_date) <= datetime.date.today():
        print("\n\t\t\t ## WARNING: THIS MEDICINE IS ALREADY EXPIRED ##")
        confirm = input("\t\t\t Do you still want to add it? (y/n): ")
        if confirm.lower() != 'y':
            return

    # Medicine Type
    try:
        m_type = int(input("\n\t\t\t Enter type of medicine (0-Syrup/1-Tablet): "))
        if m_type not in [0, 1]:
            print("\n\t\t\t ## INVALID TYPE. MUST BE 0 OR 1 ##")
            input("\n\t\t\t\t...:::::Press Enter Key:::::...")
            return
    except ValueError:
        print("\n\t\t\t ## INVALID INPUT ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    # Price and Quantity
    try:
        unit = "strip" if m_type == 1 else "bottle"
        price = float(input(f"\n\t\t\t Enter Price per {unit}: "))
        if price <= 0:
            print("\n\t\t\t ## PRICE MUST BE POSITIVE ##")
            input("\n\t\t\t\t...:::::Press Enter Key:::::...")
            return
            
        total_qty = int(input(f"\n\t\t\t Enter number of {unit}s: "))
        if total_qty <= 0:
            print("\n\t\t\t ## QUANTITY MUST BE POSITIVE ##")
            input("\n\t\t\t\t...:::::Press Enter Key:::::...")
            return
    except ValueError:
        print("\n\t\t\t ## INVALID NUMERICAL INPUT ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    amount = total_qty * price
    print(f"\n\t\t\t TOTAL AMOUNT: ₹{amount:.2f}")

    medicines.append([m_id, m_name, m_brand, man_date, exp_date, 
                     m_type, total_qty, price, amount])

    if save_medicines(medicines):
        print("\n\t\t\t ## MEDICINE ADDED SUCCESSFULLY ## ")
    
    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def search_medicine() -> None:
    """Search for a medicine in the database"""
    medicines = load_medicines()
    
    if not medicines:
        print("\n\t\t ## NO MEDICINES IN DATABASE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    print("\n\n\t#################### SEARCH SCREEN ####################")
    m_name = input('\n\t\t ENTER MEDICINE NAME: ').strip()
    
    if not m_name:
        print("\n\t\t ## PLEASE ENTER A MEDICINE NAME ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return
    
    found = False

    print(f"\n{'MED ID':<10}{'MEDICINE NAME':<20}{'BRAND':<15}{'EXPIRY DATE':<15}{'QTY':<8}{'TYPE':<10}{'PRICE':<10}{'AMOUNT':<10}")
    print('-' * 100)

    for med in medicines:
        if m_name.upper() in med[1].upper():
            m_type_name = get_medicine_type_name(med[5])
            print(f"{med[0]:<10}{med[1]:<20}{med[2]:<15}{med[4]:<15}{med[6]:<8}{m_type_name:<10}₹{med[7]:<9.2f}₹{med[8]:<9.2f}")
            found = True

    if not found:
        print("\n\t\t ## MEDICINE NOT FOUND ##")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def view_all_medicines() -> None:
    """Display all medicines in the database"""
    medicines = load_medicines()
    
    if not medicines:
        print("\n\t\t ## NO MEDICINES IN DATABASE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    print("\n\n\t#################### ALL MEDICINES ####################")
    print(f"\n{'MED ID':<10}{'MEDICINE NAME':<20}{'BRAND':<15}{'EXPIRY DATE':<15}{'QTY':<8}{'TYPE':<10}{'PRICE':<10}{'AMOUNT':<10}")
    print('-' * 100)

    for med in medicines:
        m_type_name = get_medicine_type_name(med[5])
        print(f"{med[0]:<10}{med[1]:<20}{med[2]:<15}{med[4]:<15}{med[6]:<8}{m_type_name:<10}₹{med[7]:<9.2f}₹{med[8]:<9.2f}")

    print(f"\n\t\t Total Medicines: {len(medicines)}")
    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def update_stock() -> None:
    """Update a medicine's stock quantity"""
    medicines = load_medicines()
    
    if not medicines:
        print("\n\t\t ## NO MEDICINES IN DATABASE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    print("\n\n\t#################### UPDATE STOCK SCREEN ####################")
    m_name = input('\n\t\t ENTER MEDICINE NAME: ').strip()
    
    if not m_name:
        print("\n\t\t ## PLEASE ENTER A MEDICINE NAME ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return
    
    found = False

    print(f"\n{'MED ID':<10}{'MEDICINE NAME':<20}{'EXPIRY DATE':<15}{'QTY':<8}{'TYPE':<10}{'PRICE':<10}{'AMOUNT':<10}")
    print('-' * 95)

    for i, med in enumerate(medicines):
        if m_name.upper() in med[1].upper():
            m_type_name = get_medicine_type_name(med[5])
            print(f"{med[0]:<10}{med[1]:<20}{med[4]:<15}{med[6]:<8}{m_type_name:<10}₹{med[7]:<9.2f}₹{med[8]:<9.2f}")
            
            try:
                new_q = int(input("\nEnter quantity to add (negative to reduce): "))
                new_total = medicines[i][6] + new_q
                
                if new_total < 0:
                    print("\n\t\t ## CANNOT REDUCE BELOW ZERO ##")
                else:
                    medicines[i][6] = new_total
                    medicines[i][8] = medicines[i][6] * medicines[i][7]
                    
                    if save_medicines(medicines):
                        print("\n\t\t ## STOCK UPDATED SUCCESSFULLY ##")
                        print(f"\t\t New Quantity: {medicines[i][6]}")
                        print(f"\t\t New Amount: ₹{medicines[i][8]:.2f}")
                    
            except ValueError:
                print("\n\t\t ## INVALID INPUT ##")
            
            found = True
            break

    if not found:
        print("\n\t\t ## MEDICINE NOT FOUND ##")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def delete_medicine() -> None:
    """Delete a medicine from the records"""
    medicines = load_medicines()
    
    if not medicines:
        print("\n\t\t ## NO MEDICINES IN DATABASE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    print("\n\n\t#################### DELETE MEDICINE SCREEN ####################")
    m_name = input('\n\t\t ENTER MEDICINE NAME: ').strip()
    
    if not m_name:
        print("\n\t\t ## PLEASE ENTER A MEDICINE NAME ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return
    
    found = False

    print(f"\n{'MED ID':<10}{'MEDICINE NAME':<20}{'EXPIRY DATE':<15}{'QTY':<8}{'TYPE':<10}{'PRICE':<10}{'AMOUNT':<10}")
    print('-' * 95)

    for i, med in enumerate(medicines):
        if m_name.upper() in med[1].upper():
            m_type_name = get_medicine_type_name(med[5])
            print(f"{med[0]:<10}{med[1]:<20}{med[4]:<15}{med[6]:<8}{m_type_name:<10}₹{med[7]:<9.2f}₹{med[8]:<9.2f}")
            
            ans = input(f"\nAre you sure you want to delete '{med[1]}'? (y/n): ")
            if ans.lower() == 'y':
                medicines.pop(i)
                if save_medicines(medicines):
                    print("\n\t\t ## MEDICINE DELETED SUCCESSFULLY ##")
            else:
                print("\n\t\t ## DELETION CANCELLED ##")
            
            found = True
            break

    if not found:
        print("\n\t\t ## MEDICINE NOT FOUND ##")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def get_medicine_by_name(medicines: List[List[Any]], m_name: str) -> Optional[Dict[str, Any]]:
    """Get medicine details by name"""
    for med in medicines:
        if m_name.lower() in med[1].lower():
            return {
                'id': med[0],
                'name': med[1],
                'brand': med[2],
                'quantity': med[6],
                'price': med[7],
                'type': med[5]
            }
    return None


def record_transaction(filename: str, med_name: str, qty: int, amount: float) -> bool:
    """Record a transaction (sale or return)"""
    try:
        with open(filename, "ab") as f:
            pickle.dump([datetime.date.today(), med_name, qty, amount], f)
        return True
    except Exception as e:
        print(f"\n\t\t ## ERROR RECORDING TRANSACTION: {e} ##")
        return False


def sell_medicine() -> None:
    """Sell medicine and update inventory"""
    medicines = load_medicines()
    
    if not medicines:
        print("\n\t\t ## NO MEDICINES IN DATABASE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    print("\n\n\t#################### SELL MEDICINE SCREEN ####################")
    m_name = input('\n\t\t ENTER MEDICINE NAME: ').strip()
    
    if not m_name:
        print("\n\t\t ## PLEASE ENTER A MEDICINE NAME ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return
    
    medicine = get_medicine_by_name(medicines, m_name)

    if medicine:
        unit = "strip" if medicine['type'] == 1 else "bottle"
        print(f"\n\t\t Medicine: {medicine['name']}")
        print(f"\t\t Available Stock: {medicine['quantity']} {unit}s")
        print(f"\t\t Price per {unit}: ₹{medicine['price']:.2f}")
        
        try:
            qty = int(input(f"\n\t\t Enter number of {unit}s to sell: "))
            
            if qty <= 0:
                print("\n\t\t ## QUANTITY MUST BE POSITIVE ##")
            elif qty <= medicine['quantity']:
                amount = qty * medicine['price']
                print(f"\n\t\t\t TOTAL AMOUNT: ₹{amount:.2f}")
                
                confirm = input("\n\t\t Confirm sale? (y/n): ")
                if confirm.lower() == 'y':
                    # Record sale
                    if record_transaction("sales.dat", medicine['name'], qty, amount):
                        # Update inventory
                        for med in medicines:
                            if medicine['name'].lower() == med[1].lower():
                                med[6] -= qty
                                med[8] = med[6] * med[7]
                                break
                        
                        if save_medicines(medicines):
                            print("\n\t\t ## MEDICINE SOLD SUCCESSFULLY ##")
                            print(f"\t\t Remaining Stock: {medicine['quantity'] - qty} {unit}s")
                else:
                    print("\n\t\t ## SALE CANCELLED ##")
            else:
                print(f"\n\t\t ## NOT ENOUGH STOCK. CURRENT STOCK: {medicine['quantity']} {unit}s ##")
        except ValueError:
            print("\n\t\t ## INVALID INPUT ##")
    else:
        print("\n\t\t ## MEDICINE NOT FOUND ##")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def return_medicine() -> None:
    """Return a medicine (for expiry or damage)"""
    medicines = load_medicines()
    
    if not medicines:
        print("\n\t\t ## NO MEDICINES IN DATABASE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    print("\n\n\t#################### RETURN MEDICINE SCREEN ####################")
    m_name = input('\n\t\t ENTER MEDICINE NAME: ').strip()
    
    if not m_name:
        print("\n\t\t ## PLEASE ENTER A MEDICINE NAME ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return
    
    medicine = get_medicine_by_name(medicines, m_name)

    if medicine:
        unit = "strip" if medicine['type'] == 1 else "bottle"
        print(f"\n\t\t Medicine: {medicine['name']}")
        print(f"\t\t Available Stock: {medicine['quantity']} {unit}s")
        print(f"\t\t Price per {unit}: ₹{medicine['price']:.2f}")
        
        try:
            qty = int(input(f"\n\t\t Enter number of {unit}s to return: "))
            
            if qty <= 0:
                print("\n\t\t ## QUANTITY MUST BE POSITIVE ##")
            elif qty <= medicine['quantity']:
                amount = qty * medicine['price']
                print(f"\n\t\t\t TOTAL AMOUNT TO BE RETURNED: ₹{amount:.2f}")
                
                reason = input("\n\t\t Reason for return (expiry/damage/other): ").strip()
                confirm = input("\n\t\t Confirm return? (y/n): ")
                
                if confirm.lower() == 'y':
                    # Record return
                    if record_transaction("return.dat", medicine['name'], qty, amount):
                        # Update inventory
                        for med in medicines:
                            if medicine['name'].lower() == med[1].lower():
                                med[6] -= qty
                                med[8] = med[6] * med[7]
                                break
                        
                        if save_medicines(medicines):
                            print("\n\t\t ## MEDICINE RETURNED SUCCESSFULLY ##")
                            print(f"\t\t Remaining Stock: {medicine['quantity'] - qty} {unit}s")
                else:
                    print("\n\t\t ## RETURN CANCELLED ##")
            else:
                print(f"\n\t\t ## NOT ENOUGH STOCK TO RETURN. CURRENT STOCK: {medicine['quantity']} {unit}s ##")
        except ValueError:
            print("\n\t\t ## INVALID INPUT ##")
    else:
        print("\n\t\t ## MEDICINE NOT FOUND ##")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def expiry_list() -> None:
    """Display medicines expiring within the next 30 days"""
    medicines = load_medicines()
    
    if not medicines:
        print("\n\t\t ## NO MEDICINES IN DATABASE ##")
        input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        return

    print("\n\n\t#################### UPCOMING EXPIRY MEDICINES ####################")
    print("\t\t (Medicines expiring within 30 days)")
    
    current_date = datetime.date.today()
    threshold_date = current_date + datetime.timedelta(days=30)
    found = False

    print(f"\n{'MED ID':<10}{'MEDICINE NAME':<20}{'BRAND':<15}{'EXPIRY DATE':<15}{'DAYS LEFT':<12}{'QTY':<8}{'TYPE':<10}")
    print('-' * 95)

    for med in medicines:
        try:
            exp_date = parse_date(med[4])
            days_left = (exp_date - current_date).days
            
            if exp_date <= threshold_date:
                m_type_name = get_medicine_type_name(med[5])
                status = "EXPIRED" if days_left < 0 else f"{days_left} days"
                print(f"{med[0]:<10}{med[1]:<20}{med[2]:<15}{med[4]:<15}{status:<12}{med[6]:<8}{m_type_name:<10}")
                found = True
        except Exception as e:
            print(f"\t\t ## ERROR PROCESSING MEDICINE ID {med[0]}: {e} ##")

    if not found:
        print("\n\t\t ## NO UPCOMING EXPIRY MEDICINES ##")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def main():
    """Main program loop"""
    while True:
        try:
            show_menu()
            choice = input("\n\t\t ENTER YOUR CHOICE: ").strip()
            
            if not choice.isdigit():
                print("\n\t\t\t ## PLEASE ENTER A VALID NUMBER ##")
                input("\n\t\t\t\t...:::::Press Enter Key:::::...")
                continue
            
            choice = int(choice)
            
            if choice == 0:
                print("\n\t\t\t ## THANK YOU FOR USING THE SYSTEM ##")
                break
            elif choice == 1:
                add_stock()
            elif choice == 2:
                update_stock()
            elif choice == 3:
                delete_medicine()
            elif choice == 4:
                sell_medicine()
            elif choice == 5:
                return_medicine()
            elif choice == 6:
                expiry_list()
            elif choice == 7:
                search_medicine()
            elif choice == 8:
                view_all_medicines()
            else:
                print("\n\t\t\t ## INVALID CHOICE. PLEASE SELECT 0-8 ##")
                input("\n\t\t\t\t...:::::Press Enter Key:::::...")
        except KeyboardInterrupt:
            print("\n\n\t\t\t ## PROGRAM INTERRUPTED ##")
            break
        except Exception as e:
            print(f"\n\t\t\t ## UNEXPECTED ERROR: {e} ##")
            input("\n\t\t\t\t...:::::Press Enter Key:::::...")


if __name__ == "__main__":
    main()
