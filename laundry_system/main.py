import sys
from customer_menu import customer_signup, customer_login
from washer_menu import washer_login
from admin_menu import admin_login
from utils import clear_screen


def main_menu() -> None:
    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("  LAUNDRY SERVICE MANAGEMENT SYSTEM")
        print("=" * 50)
        print("\n1. Customer Sign Up")
        print("2. Customer Login")
        print("3. Washer Login")
        print("4. Admin Login")
        print("5. Exit")

        choice: str = input("\nEnter your choice: ")

        if choice == "1":
            customer_signup()
            input("\nPress Enter to continue...")
        elif choice == "2":
            customer_login()
            input("\nPress Enter to continue...")
        elif choice == "3":
            washer_login()
            input("\nPress Enter to continue...")
        elif choice == "4":
            admin_login()
            input("\nPress Enter to continue...")
        elif choice == "5":
            print("\nThank you for using Laundry Service Management System!")
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice! Please try again.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_menu()
