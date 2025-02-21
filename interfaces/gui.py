import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from typing import Optional, Dict, List
from ttkthemes import ThemedTk
import json
from datetime import datetime

class ModernPeriodicTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Periodic Table Information System")
        self.root.geometry("1000x700")
        
        # Initialize database connection
        self.db = DatabaseManager()
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.pack(fill="both", expand=True)
        
        # Create notebook for different views
        self.create_notebook()
        
        # Initialize history
        self.search_history = []
        
    def configure_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        
        # Configure colors
        style.configure("Title.TLabel", 
                       font=("Helvetica", 24, "bold"),
                       padding=10)
        
        style.configure("Subtitle.TLabel",
                       font=("Helvetica", 12),
                       padding=5)
        
        style.configure("Search.TFrame",
                       padding=20)
        
        style.configure("Result.TFrame",
                       padding=20)
        
        style.configure("History.TFrame",
                       padding=20)

    def create_notebook(self):
        """Create notebook with different tabs"""
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Create different tabs
        self.create_search_tab()
        self.create_periodic_table_tab()
        self.create_history_tab()
        self.create_statistics_tab()

    def create_search_tab(self):
        """Create main search tab"""
        search_frame = ttk.Frame(self.notebook, style="Search.TFrame")
        self.notebook.add(search_frame, text="Search")
        
        # Title
        title = ttk.Label(search_frame, 
                         text="Periodic Table Search",
                         style="Title.TLabel")
        title.pack(fill="x", pady=10)
        
        # Search options frame
        search_options = ttk.LabelFrame(search_frame, text="Search Options", padding=10)
        search_options.pack(fill="x", pady=5)
        
        # Grid for search options
        # Atomic Number Search
        ttk.Label(search_options, text="Atomic Number:").grid(row=0, column=0, padx=5, pady=5)
        self.atomic_number_var = tk.StringVar()
        atomic_number_entry = ttk.Entry(search_options, textvariable=self.atomic_number_var)
        atomic_number_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_options, 
                   text="Search",
                   command=self.search_by_number).grid(row=0, column=2, padx=5, pady=5)
        
        # Symbol Search
        ttk.Label(search_options, text="Element Symbol:").grid(row=1, column=0, padx=5, pady=5)
        self.symbol_var = tk.StringVar()
        symbol_entry = ttk.Entry(search_options, textvariable=self.symbol_var)
        symbol_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(search_options,
                   text="Search",
                   command=self.search_by_symbol).grid(row=1, column=2, padx=5, pady=5)

        # Quick filter buttons
        filter_frame = ttk.LabelFrame(search_frame, text="Quick Filters", padding=10)
        filter_frame.pack(fill="x", pady=5)
        
        ttk.Button(filter_frame,
                   text="S-Block Elements",
                   command=lambda: self.show_block_elements('s')).pack(side="left", padx=5)
        ttk.Button(filter_frame,
                   text="P-Block Elements",
                   command=lambda: self.show_block_elements('p')).pack(side="left", padx=5)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(search_frame, text="Element Details", padding=10)
        self.results_frame.pack(fill="both", expand=True, pady=5)
        
        # Create labels for element details with better organization
        self.create_detail_labels()

    def create_periodic_table_tab(self):
        """Create visual periodic table tab"""
        table_frame = ttk.Frame(self.notebook)
        self.notebook.add(table_frame, text="Periodic Table")
        
        # Create a grid of buttons for elements
        self.element_buttons = {}
        
        # Get all elements from database
        elements = self.db.get_all_elements()
        
        # Create element buttons with appropriate positioning
        for element in elements:
            btn = ttk.Button(table_frame,
                            text=f"{element['symbol']}\n{element['atomic_number']}",
                            command=lambda e=element: self.display_element(e))
            
            # Position button based on period and group
            row = element['period'] - 1
            col = element['group_number'] - 1
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.element_buttons[element['atomic_number']] = btn

    def create_history_tab(self):
        """Create search history tab"""
        history_frame = ttk.Frame(self.notebook, style="History.TFrame")
        self.notebook.add(history_frame, text="History")
        
        # Create treeview for history
        columns = ("Time", "Search Type", "Query", "Result")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_statistics_tab(self):
        """Create statistics and analysis tab"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")
        
        # Create statistics display
        stats_text = tk.Text(stats_frame, wrap=tk.WORD, height=20, width=60)
        stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add some basic statistics
        stats = self.db.get_statistics()
        
        stats_text.insert(tk.END, "Periodic Table Statistics\n\n")
        stats_text.insert(tk.END, f"Total Elements: {stats['total_elements']}\n")
        stats_text.insert(tk.END, f"S-Block Elements: {stats['s_block_count']}\n")
        stats_text.insert(tk.END, f"P-Block Elements: {stats['p_block_count']}\n")
        stats_text.insert(tk.END, f"\nAverage Atomic Mass: {stats['avg_atomic_mass']:.2f}\n")
        
        # Make text readonly
        stats_text.configure(state='disabled')

    def create_detail_labels(self):
        """Create organized detail labels"""
        self.detail_labels = {}
        details = [
            ("Basic Info", ["Name", "Symbol", "Atomic Number"]),
            ("Physical Properties", ["Atomic Mass", "Block"]),
            ("Structure", ["Group", "Period", "Electron Configuration"])
        ]
        
        row = 0
        for section, fields in details:
            # Section header
            ttk.Label(self.results_frame,
                     text=section,
                     style="Subtitle.TLabel").grid(row=row,
                                                 column=0,
                                                 columnspan=2,
                                                 sticky="w",
                                                 pady=(10,5))
            row += 1
            
            # Fields
            for field in fields:
                ttk.Label(self.results_frame,
                         text=f"{field}:",
                         style="Header.TLabel").grid(row=row,
                                                   column=0,
                                                   sticky="w",
                                                   padx=5,
                                                   pady=2)
                self.detail_labels[field] = ttk.Label(self.results_frame,
                                                    text="",
                                                    style="Element.TLabel")
                self.detail_labels[field].grid(row=row,
                                             column=1,
                                             sticky="w",
                                             padx=5,
                                             pady=2)
                row += 1

    def display_element(self, element: Optional[Dict]):
        """Display element details and update history"""
        if not element:
            messagebox.showinfo("Not Found", "Element not found!")
            return
        
        # Update labels
        for key, label in self.detail_labels.items():
            value = element.get(key.lower().replace(" ", "_"), "")
            label.config(text=str(value))
        
        # Add to history
        self.add_to_history("Display", f"Element: {element['symbol']}", "Success")

    def add_to_history(self, search_type: str, query: str, result: str):
        """Add search to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_tree.insert("", 0, values=(timestamp, search_type, query, result))
        
        # Keep history limited to last 10 searches
        if len(self.history_tree.get_children()) > 10:
            self.history_tree.delete(self.history_tree.get_children()[-1])

    def search_by_number(self):
        """Handle atomic number search"""
        try:
            number = int(self.atomic_number_var.get())
            element = self.db.get_element_by_number(number)
            self.display_element(element)
            self.add_to_history("Atomic Number", str(number), 
                              "Found" if element else "Not Found")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid atomic number!")

    def search_by_symbol(self):
        """Handle symbol search"""
        symbol = self.symbol_var.get().strip()
        if symbol:
            element = self.db.get_element_by_symbol(symbol)
            self.display_element(element)
            self.add_to_history("Symbol", symbol, 
                              "Found" if element else "Not Found")
        else:
            messagebox.showerror("Error", "Please enter an element symbol!")

    def show_block_elements(self, block: str):
        """Display elements in specified block"""
        elements = self.db.get_elements_by_block(block)
        self.show_elements_list(f"Elements in {block.upper()}-Block", elements)
        self.add_to_history("Block", block, f"Found {len(elements)} elements")

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
    root = ThemedTk(theme="arc")  # You can choose different themes: 'arc', 'equilux', etc.
    app = ModernPeriodicTableGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()