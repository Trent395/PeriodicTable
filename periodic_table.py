
import tkinter as tk
from tkinter import ttk, messagebox
from Elements import Elements

class PeriodicTableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Periodic Table")
        self.geometry("1600x900")  # Increase window width for better spacing
        self.configure(bg="#2e2e2e")  # Dark background

        # Initialize the Elements class
        self.elements = Elements()

        # Create a frame to wrap the periodic table and add padding
        self.table_frame = tk.Frame(self, bg="#2e2e2e", padx=20, pady=20)
        self.table_frame.grid(row=0, column=0, sticky="nsew")

        # Create labels for periods (rows) and groups (columns)
        self.create_labels()

        # Create buttons for each element
        self.create_periodic_table()

        # Create a frame to display element details
        self.details_frame = tk.Frame(self, bg="#2e2e2e")
        self.details_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Add a label to display the element details
        self.details_label = tk.Label(self.details_frame, text="", bg="#2e2e2e", fg="white", font=("Arial", 12))
        self.details_label.pack(fill="both", padx=10, pady=10)

        # Create a search bar
        self.create_search_bar()

    def create_labels(self):
        """Creates labels for groups (columns) and periods (rows) around the periodic table."""
        group_labels = ["Group " + str(i) for i in range(1, 19)]
        period_labels = ["Period " + str(i) for i in range(1, 8)]

        # Create column labels (Groups)
        for i, label in enumerate(group_labels):
            lbl = tk.Label(self.table_frame, text=label, bg="#2e2e2e", fg="white", font=("Arial", 10, "bold"))
            lbl.grid(row=0, column=i + 1, padx=10, pady=5)

        # Create row labels (Periods)
        for i, label in enumerate(period_labels):
            lbl = tk.Label(self.table_frame, text=label, bg="#2e2e2e", fg="white", font=("Arial", 10, "bold"))
            lbl.grid(row=i + 1, column=0, padx=10, pady=5)

    def create_periodic_table(self):
        """Creates buttons for each element in the periodic table layout."""
        button_width = 6  # Adjust width for space to show atomic number and mass
        
        for symbol, position in self.elements.elements.items():
            row, col = position

            # Get the color and category for the element
            color = self.elements.get_element_color(symbol)

            # Retrieve the atomic number and atomic mass for the element
            atomic_number = self.elements.get_atomic_number(symbol)
            atomic_mass = self.elements.get_atomic_mass(symbol)

            # Format atomic mass as a float, if possible, otherwise keep it as is
            try:
                atomic_mass_text = f"{float(atomic_mass):.2f}"
            except (ValueError, TypeError):
                atomic_mass_text = str(atomic_mass)

            # Create a multi-line text for the button with atomic number, symbol, and atomic mass
            button_text = f"{atomic_number}\n{symbol}\n{atomic_mass_text}"
            
            # Create the button with the formatted text
            btn = tk.Button(
                self.table_frame, text=button_text, font=("Arial", 10, "bold"), 
                bg=color, width=button_width, height=3,  # Height adjusted to fit text
                command=lambda s=symbol: self.show_element_details(s)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Add tooltip with additional information
            tooltip_text = f"{self.elements.element_names[symbol]} (Atomic Number: {atomic_number}, Atomic Mass: {atomic_mass_text} amu)"
            self.create_tooltip(btn, tooltip_text)

        # Make grid cells expand evenly
        for i in range(19):  # Number of columns (18 for elements + 1 for labels)
            self.table_frame.grid_columnconfigure(i, weight=1)
        for i in range(11):  # Number of rows (10 for elements + 1 for labels)
            self.table_frame.grid_rowconfigure(i, weight=1)


    def show_element_details(self, symbol):
        """Shows detailed information about an element in the same window below the table."""
        # Retrieve element details
        name = self.elements.element_names[symbol]
        atomic_number = self.elements.get_atomic_number(symbol)
        atomic_mass = self.elements.get_atomic_mass(symbol)
        oxidation_states = self.elements.get_oxidation_states(symbol)
        electronegativity = self.elements.get_electronegativity(symbol)
        density = self.elements.get_density(symbol)
        electron_config = self.elements.get_electron_configuration(symbol)
        category = self.elements.get_element_category(symbol)

        # Format the element properties for display in a more visually appealing way
        properties = f"""
        {name} (Symbol: {symbol})
        ---------------------------
        Atomic Number: {atomic_number}
        Atomic Mass: {atomic_mass} amu
        Category: {category}
        Oxidation States: {oxidation_states}
        Electronegativity: {electronegativity}
        Density: {density} g/cm³
        Electron Configuration: {electron_config}
        """

        # Update the details label with the element's properties
        self.details_label.config(text=properties.strip())

    def create_tooltip(self, widget, text):
        """Creates a tooltip for a widget."""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1, font=("Arial", 8))
        label.pack(ipadx=1)
        tooltip.withdraw()

        def enter(event):
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def search_element(self, event=None):
        """Search for an element by its symbol or name."""
        search_term = self.search_var.get().strip().capitalize()
        symbol = self.find_element_by_symbol_or_name(search_term)
        if symbol:
            self.show_element_details(symbol)
        else:
            messagebox.showerror("Not Found", "Element not found.")

    def find_element_by_symbol_or_name(self, search_term):
        """Find an element by its symbol or name."""
        # Search by symbol
        if search_term in self.elements.elements:
            return search_term
        
        # Search by element name
        for symbol, name in self.elements.element_names.items():
            if name.lower() == search_term.lower():
                return symbol
        
        return None

    def create_search_bar(self):
        """Creates a search bar and positions it between Be and B, directly above Mn and Fe."""
        search_frame = tk.Frame(self.table_frame, bg="#2e2e2e")
        search_frame.grid(row=2, column=7, columnspan=4, padx=5, pady=5)  # Positioned between Be and B

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<Return>", self.search_element)

        search_button = ttk.Button(search_frame, text="Search", command=self.search_element)
        search_button.pack(side=tk.LEFT, padx=5)



if __name__ == "__main__":
    app = PeriodicTableApp()
    app.mainloop()
