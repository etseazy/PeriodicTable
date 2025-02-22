import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from typing import Optional, Dict, List
from ttkthemes import ThemedTk
import customtkinter as ctk
from PIL import Image, ImageTk
import colorsys
import json
from datetime import datetime

class PeriodicTableGUI:
    def __init__(self):
        """Initialize the main window with modern styling"""
        # Set up customtkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Modern Periodic Table")
        self.root.geometry("1200x800")
        
        # Color scheme
        self.colors = {
            's': "#FF6B6B",  
            'p': "#4ECDC4",  
            'background': "#2F3542",
            'text': "#FFFFFF",
            'highlight': "#A3CB38"
        }
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Create main interface
        self.create_interface()
        
        # Initialize search history
        self.search_history = []

    def create_interface(self):
        """Create the main interface with modern styling"""
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title
        title = ctk.CTkLabel(
            self.main_container,
            text="Modern Periodic Table",
            font=("Helvetica", 28, "bold")
        )
        title.pack(pady=20)
        
        # Create tabview
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True)
        
        # Add tabs
        self.search_tab = self.tabview.add("Search")
        self.table_tab = self.tabview.add("Periodic Table")
        self.info_tab = self.tabview.add("Element Info")
        self.history_tab = self.tabview.add("History")
        
        # Set up each tab
        self.setup_search_tab()
        self.setup_table_tab()
        self.setup_info_tab()
        self.setup_history_tab()

    def setup_search_tab(self):
        """Set up the search interface"""
        # Search frame
        search_frame = ctk.CTkFrame(self.search_tab)
        search_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Search by atomic number
        number_frame = ctk.CTkFrame(search_frame)
        number_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            number_frame,
            text="Atomic Number:",
            font=("Helvetica", 14)
        ).pack(side="left", padx=10)
        
        self.atomic_number_var = tk.StringVar()
        number_entry = ctk.CTkEntry(
            number_frame,
            textvariable=self.atomic_number_var,
            width=120
        )
        number_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(
            number_frame,
            text="Search",
            command=self.search_by_number,
            font=("Helvetica", 12)
        ).pack(side="left", padx=10)
        
        # Search by symbol
        symbol_frame = ctk.CTkFrame(search_frame)
        symbol_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            symbol_frame,
            text="Element Symbol:",
            font=("Helvetica", 14)
        ).pack(side="left", padx=10)
        
        self.symbol_var = tk.StringVar()
        symbol_entry = ctk.CTkEntry(
            symbol_frame,
            textvariable=self.symbol_var,
            width=120
        )
        symbol_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(
            symbol_frame,
            text="Search",
            command=self.search_by_symbol,
            font=("Helvetica", 12)
        ).pack(side="left", padx=10)
        
        # Quick filters
        filter_frame = ctk.CTkFrame(search_frame)
        filter_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            filter_frame,
            text="Quick Filters:",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        button_frame = ctk.CTkFrame(filter_frame)
        button_frame.pack(fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="S-Block Elements",
            command=lambda: self.show_block_elements('s'),
            fg_color=self.colors['s'],
            font=("Helvetica", 12)
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="P-Block Elements",
            command=lambda: self.show_block_elements('p'),
            fg_color=self.colors['p'],
            font=("Helvetica", 12)
        ).pack(side="left", padx=10)

    def setup_table_tab(self):
        """Set up the periodic table visualization"""
        table_frame = ctk.CTkFrame(self.table_tab)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Grid for periodic table
        self.element_buttons = {}
        elements = self.db.get_all_elements()
        
        for element in elements:
            # Element button with custom styling
            btn = ctk.CTkButton(
                table_frame,
                text=f"{element['symbol']}\n{element['atomic_number']}",
                command=lambda e=element: self.display_element(e),
                width=80,
                height=80,
                fg_color=self.colors[element['block']],
                font=("Helvetica", 14, "bold")
            )
            
            # Position button based on period and group
            row = element['period'] - 1
            col = element['group_number'] - 1 if element['group_number'] else 0
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.element_buttons[element['atomic_number']] = btn

    def setup_info_tab(self):
        """Set up the element information display"""
        self.info_frame = ctk.CTkFrame(self.info_tab)
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Labels for element details
        self.detail_labels = {}
        self.create_detail_labels()

    def setup_history_tab(self):
        """Set up the search history display"""
        history_frame = ctk.CTkFrame(self.history_tab)
        history_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create history list
        self.history_list = ctk.CTkTextbox(
            history_frame,
            font=("Helvetica", 12)
        )
        self.history_list.pack(fill="both", expand=True)
        
        # Add clear history button
        ctk.CTkButton(
            history_frame,
            text="Clear History",
            command=self.clear_history,
            font=("Helvetica", 12)
        ).pack(pady=10)

    def create_detail_labels(self):
        """Create organized detail labels with modern styling"""
        self.detail_labels = {}
        details = [
            ("Basic Information", ["Name", "Symbol", "Atomic Number"]),
            ("Physical Properties", ["Atomic Mass", "Block"]),
            ("Structure", ["Group", "Period", "Electron Configuration"])
        ]
        
        for section, fields in details:
            # Section header
            frame = ctk.CTkFrame(self.info_frame)
            frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(
                frame,
                text=section,
                font=("Helvetica", 16, "bold")
            ).pack(anchor="w", padx=10, pady=5)
            
            # Fields
            for field in fields:
                field_frame = ctk.CTkFrame(frame)
                field_frame.pack(fill="x", padx=20)
                
                ctk.CTkLabel(
                    field_frame,
                    text=f"{field}:",
                    font=("Helvetica", 12)
                ).pack(side="left", padx=5)
                
                self.detail_labels[field] = ctk.CTkLabel(
                    field_frame,
                    text="",
                    font=("Helvetica", 12, "bold")
                )
                self.detail_labels[field].pack(side="left", padx=5)

    def display_element(self, element: Optional[Dict]):
        """Display element details with modern styling"""
        if not element:
            messagebox.showinfo("Not Found", "Element not found!")
            return
        
        # Update labels
        for key, label in self.detail_labels.items():
            value = element.get(key.lower().replace(" ", "_"), "")
            label.configure(text=str(value))
        
        # Switch to info tab
        self.tabview.set("Element Info")
        
        # Add to history
        self.add_to_history(f"Viewed {element['symbol']}")

    def add_to_history(self, action: str):
        """Add action to history with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_list.insert("1.0", f"{timestamp}: {action}\n")
        
    def clear_history(self):
        """Clear search history"""
        self.history_list.delete("1.0", tk.END)

    def search_by_number(self):
        """Search element by atomic number"""
        try:
            number = int(self.atomic_number_var.get())
            element = self.db.get_element_by_number(number)
            self.display_element(element)
            self.add_to_history(f"Searched atomic number: {number}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid atomic number!")

    def search_by_symbol(self):
        """Search element by symbol"""
        symbol = self.symbol_var.get().strip()
        if symbol:
            element = self.db.get_element_by_symbol(symbol)
            self.display_element(element)
            self.add_to_history(f"Searched symbol: {symbol}")
        else:
            messagebox.showerror("Error", "Please enter an element symbol!")

    def show_block_elements(self, block: str):
        """Display elements in specified block"""
        elements = self.db.get_elements_by_block(block)
        self.show_elements_list(f"Elements in {block.upper()}-Block", elements)
        self.add_to_history(f"Viewed {block}-block elements")

    def show_elements_list(self, title: str, elements: List[Dict]):
        """Show list of elements in a modern popup window"""
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("400x600")

        # Bring popup to front
        popup.lift()  # Lifts the window to the top
        popup.focus_force()  # Forces focus on the popup window
        
        # Create scrollable frame
        frame = ctk.CTkScrollableFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add elements
        for element in elements:
            element_frame = ctk.CTkFrame(frame)
            element_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                element_frame,
                text=f"{element['symbol']} - {element['name']}",
                font=("Helvetica", 14, "bold")
            ).pack(pady=5)
            
            ctk.CTkLabel(
                element_frame,
                text=f"Atomic Number: {element['atomic_number']}",
                font=("Helvetica", 12)
            ).pack()

    def run(self):
        """Start the application"""
        self.root.mainloop()

class DatabaseManager:
    def __init__(self):
        """Initialize database connection"""
        try:
            self.conn_str = (
                "Driver={SQL Server};"
                "Server=localhost;"
                "Database=PeriodicTableDB;"
                "Trusted_Connection=yes;"
            )
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to connect to database: {str(e)}")
            raise

    def get_all_elements(self) -> List[Dict]:
        """Get all elements from the database"""
        try:
            self.cursor.execute("""
                SELECT * FROM Elements 
                ORDER BY AtomicNumber
            """)
            return self._fetch_all_elements()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to fetch elements: {str(e)}")
            return []

    def get_element_by_number(self, atomic_number: int) -> Optional[Dict]:
        """Get element details by atomic number"""
        try:
            self.cursor.execute("EXEC GetElementByNumber ?", atomic_number)
            return self._fetch_element_dict()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to fetch element: {str(e)}")
            return None

    def get_element_by_symbol(self, symbol: str) -> Optional[Dict]:
        """Get element details by symbol"""
        try:
            self.cursor.execute("EXEC GetElementBySymbol ?", symbol)
            return self._fetch_element_dict()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to fetch element: {str(e)}")
            return None

    def get_elements_by_block(self, block: str) -> List[Dict]:
        """Get all elements in a specific block"""
        try:
            self.cursor.execute("EXEC GetElementsByBlock ?", block)
            return self._fetch_all_elements()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to fetch elements: {str(e)}")
            return []

    def get_elements_by_period(self, period: int) -> List[Dict]:
        """Get all elements in a specific period"""
        try:
            self.cursor.execute("EXEC GetElementsByPeriod ?", period)
            return self._fetch_all_elements()
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to fetch elements: {str(e)}")
            return []

    def get_statistics(self) -> Dict:
        """Get statistical information about the elements"""
        try:
            stats = {}
            
            # Get total count
            self.cursor.execute("SELECT COUNT(*) FROM Elements")
            stats['total_elements'] = self.cursor.fetchone()[0]
            
            # Get block counts
            self.cursor.execute("SELECT COUNT(*) FROM Elements WHERE Block = 's'")
            stats['s_block_count'] = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM Elements WHERE Block = 'p'")
            stats['p_block_count'] = self.cursor.fetchone()[0]
            
            # Get average atomic mass
            self.cursor.execute("SELECT AVG(AtomicMass) FROM Elements")
            stats['avg_atomic_mass'] = float(self.cursor.fetchone()[0])
            
            return stats
        except pyodbc.Error as e:
            messagebox.showerror("Database Error", 
                               f"Failed to fetch statistics: {str(e)}")
            return {
                'total_elements': 0,
                's_block_count': 0,
                'p_block_count': 0,
                'avg_atomic_mass': 0.0
            }

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

    def __del__(self):
        """Close database connection"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
        except:
            pass

def main():
    app = PeriodicTableGUI()
    app.run()

if __name__ == "__main__":
    main()