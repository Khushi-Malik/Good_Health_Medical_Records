import pickle
import os
import datetime
from typing import Optional, Any
import math


def show_menu() -> None:
    """To display the instructions and features of the program"""
    print("*" * 20, end='')
    print("  GOOD HEALTH FAMILY MEDICAL STORE  ", end="")
    print("*" * 20, end='')
    print("\n\n")
    print("\t\t\t 1. ADD STOCK ")
    print("\t\t\t 2. UPDATE STOCK ")
    print("\t\t\t 3. DELETE MEDICINE ")
    print("\t\t\t 4. SELL MEDICINE ")
    print("\t\t\t 5. RETURN MEDICINE ")
    print("\t\t\t 6. UPCOMING EXPIRY MEDICINE LIST ")
    print("\t\t\t 7. SEARCH MEDICINE ")
    print("\t\t\t 0. EXIT ")
    print("\n" * 2)
    print(" " * 20, end="")


def medicine_expired(date: datetime.date) -> bool:
    """To check if the medicine has expired or not"""
    return date <= datetime.date.today()


def check_valid_date(date: str) -> bool:
    """To check if an input date is valid"""
    try:
        datetime.datetime.strptime(date, "%Y, %m, %d")
        return True
    except ValueError:
        return False


def add_stock() -> None:
    """Add medicines in the database."""
    if os.path.exists('Medicines.dat'):
        with open("Medicines.dat", "rb") as f:
            medicines = pickle.load(f)
        m_id = len(medicines) + 1
    else:
        medicines = []
        m_id = 1

    print('\n\n\t\t\t Medicine ID: ', m_id)
    m_name = input('\n\n\t\t\t Enter Medicine Name: ')
    m_brand = input('\n\n\t\t\t Enter Medicine Brand Name: ')

    man_date = input('\n\n\t\t\t Enter Medicine Manufacturing Date (yyyy, mm, dd): ')
    while not check_valid_date(man_date):
        print("\t\t\t ## INVALID DATE ##")
        man_date = input('\n\n\t\t\t Enter Medicine Manufacturing Date (yyyy, mm, dd): ')

    exp_date = input('\n\n\t\t\t Enter Medicine Expiry Date (yyyy, mm, dd): ')
    while not check_valid_date(exp_date):
        print("\t\t\t ## INVALID DATE ##")
        exp_date = input('\n\n\t\t\t Enter Medicine Expiry Date (yyyy, mm, dd): ')

    m_type = int(input("\n\n\t\t\t Enter type of medicine (0-Syrup/1-Tablet): "))
    price = 0.0
    total_qty = 0

    if m_type == 1:
        price = float(input("\n\n\t\t\t Enter Price per strip: "))
        total_qty = int(input("\n\n\t\t\t Enter number of strips: "))
    elif m_type == 0:
        price = float(input("\n\n\t\t\t Enter Price per bottle: "))
        total_qty = int(input("\n\n\t\t\t Enter number of bottles: "))

    amount = total_qty * price
    print(f"\n\n\t\t\t TOTAL AMOUNT: {amount}")

    medicines.append([m_id, m_name, m_brand, man_date, exp_date, m_type, total_qty, price, amount])

    with open("Medicines.dat", "wb") as f:
        pickle.dump(medicines, f)
    print("\n\n\t\t\t ## DATA SAVED ## ")
    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def search_medicine() -> None:
    """To search for a medicine in the file"""
    if os.path.exists("Medicines.dat"):
        with open("Medicines.dat", "rb") as f:
            medicines = pickle.load(f)

        print("\n\n\t#################### SEARCH SCREEN ####################")
        m_name = input('\n\n\t\t ENTER MEDICINE NAME: ')
        found = False

        print('%7s' % 'MED ID', '%15s' % 'MEDICINE NAME', '%12s' % 'EXPIRY DATE', '%5s' % 'QTY', '%10s' % 'TYPE', '%8s' % 'AMOUNT')
        print('-' * 80)

        for med in medicines:
            if m_name.upper() in med[1].upper():
                print('%7s' % med[0], '%15s' % med[1], '%12s' % med[4], '%5s' % med[6], '%10s' % med[5], '%8s' % med[8])
                found = True

        if not found:
            print("\n\t\t ## MEDICINE NOT FOUND ##")

    else:
        print("\n\t\t ## FILE NOT FOUND ## ")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def update_stock() -> None:
    """To update a medicine's data."""
    if os.path.exists("Medicines.dat"):
        with open("Medicines.dat", "rb") as f:
            medicines = pickle.load(f)

        print("\n\n\t#################### UPDATE STOCK SCREEN ####################")
        m_name = input('\n\n\t\t ENTER MEDICINE NAME: ')
        found = False

        print('%7s' % 'MED ID', '%15s' % 'MEDICINE NAME', '%12s' % 'EXPIRY DATE', '%5s' % 'QTY', '%10s' % 'TYPE', '%8s' % 'PRICE', '%8s' % 'AMOUNT')
        print('-' * 80)

        for i, med in enumerate(medicines):
            if m_name.upper() in med[1].upper():
                print('%7s' % med[0], '%15s' % med[1], '%12s' % med[4], '%5s' % med[6], '%10s' % med[5], '%8s' % med[7], '%8s' % med[8])
                new_q = int(input("Enter new quantity to add: "))
                medicines[i][6] += new_q
                medicines[i][8] = medicines[i][6] * medicines[i][7]
                print("\n\n## STOCK UPDATED ##")
                found = True
                break

        if not found:
            print("\n\t\t ## MEDICINE NOT FOUND ##")

        with open("Medicines.dat", "wb") as f:
            pickle.dump(medicines, f)

    else:
        print("\n\t\t ## FILE NOT FOUND ## ")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def delete_medicine() -> None:
    """To delete a medicine from the records."""
    if os.path.exists("Medicines.dat"):
        with open("Medicines.dat", "rb") as f:
            medicines = pickle.load(f)

        print("\n\n\t#################### DELETE MEDICINE SCREEN ####################")
        m_name = input('\n\n\t\t ENTER MEDICINE NAME: ')
        found = False

        print('%7s' % 'MED ID', '%15s' % 'MEDICINE NAME', '%12s' % 'EXPIRY DATE', '%5s' % 'QTY', '%10s' % 'TYPE', '%8s' % 'PRICE', '%8s' % 'AMOUNT')
        print('-' * 80)

        for i, med in enumerate(medicines):
            if m_name.upper() in med[1].upper():
                print('%7s' % med[0], '%15s' % med[1], '%12s' % med[4], '%5s' % med[6], '%10s' % med[5], '%8s' % med[7], '%8s' % med[8])
                ans = input(f"Are you sure you want to delete {m_name}? (y/n) ")
                if ans.lower() == 'y':
                    medicines.pop(i)
                    print("\n ## MEDICINE DELETED SUCCESSFULLY ##")
                found = True
                break

        if not found:
            print("\n\t\t ## MEDICINE NOT FOUND ##")

        with open("Medicines.dat", "wb") as f:
            pickle.dump(medicines, f)

    else:
        print("\n\t\t ## FILE NOT FOUND ## ")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def get_quantity_rate(medicines: list[list], m_name: str) -> Optional[tuple]:
    for med in medicines:
        if m_name.lower() in med[1].lower():
            return med[6], med[7], med[6], med[1]
    return None


def sell_medicine() -> None:
    """Sell medicine"""
    if os.path.exists("Medicines.dat"):
        with open("Medicines.dat", "rb") as f:
            medicines = pickle.load(f)

        print("\n\n\t#################### SELL MEDICINE SCREEN ####################")
        m_name = input('\n\n\t\t ENTER MEDICINE NAME: ')
        result = get_quantity_rate(medicines, m_name)

        if result is not None:
            quantity, rate, stock_qty, med_name = result
            qty = int(input(f"Enter number of bottles/strips of {med_name} to sell: "))
            if qty <= quantity:
                amount = qty * rate
                print(f"\n\n\t\t\t TOTAL AMOUNT: {amount}")
                with open("sales.dat", "ab") as f:
                    pickle.dump([datetime.date.today(), med_name, qty, amount], f)
                for med in medicines:
                    if med_name.lower() in med[1].lower():
                        med[6] -= qty
                        med[8] = med[6] * med[7]
                        break
                with open("Medicines.dat", "wb") as f:
                    pickle.dump(medicines, f)
                print("\n\n\t\t\t ## MEDICINE SOLD SUCCESSFULLY ##")
            else:
                print(f"\n\n\t\t\t ## NOT ENOUGH STOCK. CURRENT STOCK: {stock_qty} ##")
        else:
            print("\n\n\t\t\t ## MEDICINE NOT FOUND ##")

    else:
        print("\n\t\t ## FILE NOT FOUND ## ")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def return_medicine() -> None:
    """To return a medicine in case of expiry or damage"""
    if os.path.exists("Medicines.dat"):
        with open("Medicines.dat", "rb") as f:
            medicines = pickle.load(f)

        print("\n\n\t#################### RETURN MEDICINE SCREEN ####################")
        m_name = input('\n\n\t\t ENTER MEDICINE NAME: ')
        result = get_quantity_rate(medicines, m_name)

        if result is not None:
            quantity, rate, stock_qty, med_name = result
            qty = int(input(f"Enter number of bottles/strips of {med_name} to return: "))
            if qty <= quantity:
                amount = qty * rate
                print(f"\n\n\t\t\t TOTAL AMOUNT TO BE RETURNED: {amount}")
                with open("return.dat", "ab") as f:
                    pickle.dump([datetime.date.today(), med_name, qty, amount], f)
                for med in medicines:
                    if med_name.lower() in med[1].lower():
                        med[6] -= qty
                        med[8] = med[6] * med[7]
                        break
                with open("Medicines.dat", "wb") as f:
                    pickle.dump(medicines, f)
                print("\n\n\t\t\t ## MEDICINE RETURNED SUCCESSFULLY ##")
            else:
                print(f"\n\n\t\t\t ## NOT ENOUGH STOCK TO RETURN. CURRENT STOCK: {stock_qty} ##")
        else:
            print("\n\n\t\t\t ## MEDICINE NOT FOUND ##")

    else:
        print("\n\t\t ## FILE NOT FOUND ## ")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def expiry_list() -> None:
    """To display the list of upcoming expiry medicines"""
    if os.path.exists("Medicines.dat"):
        with open("Medicines.dat", "rb") as f:
            medicines = pickle.load(f)

        print("\n\n\t#################### UPCOMING EXPIRY MEDICINES ####################")
        current_date = datetime.date.today()
        found = False

        print('%7s' % 'MED ID', '%15s' % 'MEDICINE NAME', '%12s' % 'EXPIRY DATE', '%5s' % 'QTY', '%10s' % 'TYPE', '%8s' % 'AMOUNT')
        print('-' * 80)

        for med in medicines:
            exp_date = datetime.datetime.strptime(med[4], "%Y, %m, %d").date()
            if exp_date <= current_date + datetime.timedelta(days=30):
                print('%7s' % med[0], '%15s' % med[1], '%12s' % med[4], '%5s' % med[6], '%10s' % med[5], '%8s' % med[8])
                found = True

        if not found:
            print("\n\t\t ## NO UPCOMING EXPIRY MEDICINES ##")

    else:
        print("\n\t\t ## FILE NOT FOUND ## ")

    input("\n\t\t\t\t...:::::Press Enter Key:::::...")


def main():
    while True:
        show_menu()
        choice = int(input("\n\t\t ENTER YOUR CHOICE: "))
        if choice == 0:
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
        else:
            print("\n\t\t\t ## INVALID CHOICE ##")
            input("\n\t\t\t\t...:::::Press Enter Key:::::...")


if __name__ == "__main__":
    main()
