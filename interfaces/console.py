import pyodbc
from typing import Optional, List, Dict
import os

class PeriodicTableSystem:
    def __init__(self):
        """Initialize database connection"""
        # Update these connection details according to your SQL Server setup
        self.conn_str = (
            "Driver={SQL Server};"
            "Server=localhost;"
            "Database=PeriodicTableDB;"
            "Trusted_Connection=yes;"
        )
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

    def get_element_by_number(self, atomic_number: int) -> Optional[Dict]:
        """Get element details by atomic number using stored procedure"""
        self.cursor.execute("EXEC GetElementByNumber ?", atomic_number)
        return self._fetch_element_dict()

    def get_element_by_symbol(self, symbol: str) -> Optional[Dict]:
        """Get element details by symbol using stored procedure"""
        self.cursor.execute("EXEC GetElementBySymbol ?", symbol)
        return self._fetch_element_dict()

    def get_elements_by_block(self, block: str) -> List[Dict]:
        """Get all elements in a specific block using stored procedure"""
        self.cursor.execute("EXEC GetElementsByBlock ?", block)
        return self._fetch_all_elements()

    def get_elements_by_period(self, period: int) -> List[Dict]:
        """Get all elements in a specific period using stored procedure"""
        self.cursor.execute("EXEC GetElementsByPeriod ?", period)
        return self._fetch_all_elements()

    def _fetch_element_dict(self) -> Optional[Dict]:
        """Convert a single row to dictionary"""
        row = self.cursor.fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    def _fetch_all_elements(self) -> List[Dict]:
        """Convert multiple rows to list of dictionaries"""
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]

    def _row_to_dict(self, row) -> Dict:
        """Convert a row to a dictionary"""
        return {
            "atomic_number": row[0],
            "symbol": row[1],
            "name": row[2],
            "atomic_mass": float(row[3]),
            "block": row[4],
            "group_number": row[5],
            "period": row[6],
            "electron_configuration": row[7]
        }

    def close(self):
        """Close database connection"""
        self.conn.close()

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu"""
    print("\n=== Periodic Table Information System ===")
    print("1. Search by Atomic Number")
    print("2. Search by Symbol")
    print("3. View elements by Block (s/p)")
    print("4. View elements by Period")
    print("5. Exit")
    print("=======================================")

def display_element(element: Dict):
    """Display element details in a formatted way"""
    if not element:
        print("\nElement not found!")
        return
    
    print("\n=== Element Details ===")
    print(f"Name: {element['name']}")
    print(f"Symbol: {element['symbol']}")
    print(f"Atomic Number: {element['atomic_number']}")
    print(f"Atomic Mass: {element['atomic_mass']:.4f}")
    print(f"Block: {element['block']}")
    print(f"Group: {element['group_number']}")
    print(f"Period: {element['period']}")
    print(f"Electron Configuration: {element['electron_configuration']}")
    print("=====================")

def main():
    db = PeriodicTableSystem()
    
    while True:
        clear_screen()
        display_menu()
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            try:
                atomic_number = int(input("\nEnter atomic number: "))
                element = db.get_element_by_number(atomic_number)
                display_element(element)
            except ValueError:
                print("\nPlease enter a valid number!")

        elif choice == '2':
            symbol = input("\nEnter element symbol: ").strip()
            element = db.get_element_by_symbol(symbol)
            display_element(element)

        elif choice == '3':
            block = input("\nEnter block (s/p): ").strip().lower()
            if block in ['s', 'p']:
                elements = db.get_elements_by_block(block)
                print(f"\n=== Elements in {block.upper()}-block ===")
                for element in elements:
                    print(f"{element['symbol']}: {element['name']}")
            else:
                print("\nInvalid block! Please enter 's' or 'p'")

        elif choice == '4':
            try:
                period = int(input("\nEnter period number: "))
                elements = db.get_elements_by_period(period)
                print(f"\n=== Elements in Period {period} ===")
                for element in elements:
                    print(f"{element['symbol']}: {element['name']}")
            except ValueError:
                print("\nPlease enter a valid number!")

        elif choice == '5':
            print("\nThank you for using the Periodic Table Information System!")
            db.close()
            break

        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()1