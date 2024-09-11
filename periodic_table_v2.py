import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from dark_mode_manager import DarkModeManager  # Import the dark mode manager
from elements import Elements  # Assuming this is the same Elements class from before

class PeriodicTableApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern Periodic Table")
        self.setMinimumSize(1600, 900)

        # Initialize the Elements class
        self.elements = Elements()

        # Initialize DarkModeManager and apply dark mode
        self.dark_mode_manager = DarkModeManager()
        self.dark_mode_manager.apply_palette()

        # Set up the grid layout for the periodic table
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)

        # Create labels for periods (rows) and groups (columns)
        self.create_labels()

        # Create buttons for each element
        self.create_periodic_table()

        # Create a layout for the search bar and element details
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.grid_layout)

        # Create a search bar
        self.create_search_bar()

        # Label for element details
        self.details_label = QLabel("")
        self.details_label.setStyleSheet("color: white;")
        self.details_label.setFont(QFont("Arial", 12))
        self.main_layout.addWidget(self.details_label)

        self.setLayout(self.main_layout)

        # Set initial scaling to avoid button overlapping
        self.resizeEvent = self.on_resize  # Hook resize event to handle dynamic scaling

    def create_labels(self):
        """Create labels for groups (columns) and periods (rows) around the periodic table."""
        group_labels = ["Group " + str(i) for i in range(1, 19)]
        period_labels = ["Period " + str(i) for i in range(1, 8)]

        # Create column labels (Groups)
        for i, label in enumerate(group_labels):
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: white; font-weight: bold;")
            self.grid_layout.addWidget(lbl, 0, i + 1)

        # Create row labels (Periods)
        for i, label in enumerate(period_labels):
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: white; font-weight: bold;")
            self.grid_layout.addWidget(lbl, i + 1, 0)

    def create_periodic_table(self):
        """Create buttons for each element in the periodic table layout."""
        for symbol, position in self.elements.elements.items():
            row, col = position

            # Get the color and category for the element
            color = self.elements.get_element_color(symbol)

            # Retrieve the atomic number and atomic mass for the element
            atomic_number = self.elements.get_atomic_number(symbol)
            atomic_mass = self.elements.get_atomic_mass(symbol)

            # Create button text
            button_text = f"{atomic_number}\n{symbol}\n{atomic_mass}"

            # Create the button for the element
            button = QPushButton(button_text)
            button.setStyleSheet(f"background-color: {color}; color: black;")
            button.setFont(QFont("Arial", 10, QFont.Bold))

            # Set button action to show element details
            button.clicked.connect(lambda _, s=symbol: self.show_element_details(s))

            # Add button to grid
            self.grid_layout.addWidget(button, row, col)

        # Add a gap row between the bottom two rows
        self.grid_layout.setRowMinimumHeight(8, 30)  # Gap row

    def on_resize(self, event):
        """Adjust button sizes and font based on window resizing."""
        total_width = self.width()
        total_height = self.height()

        # Adjust button size based on window size
        button_size = QSize(total_width // 25, total_height // 20)  # Dynamically calculate button size

        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setFixedSize(button_size)

                # Adjust font size dynamically
                font_size = max(button_size.height() // 6, 8)  # Ensure font size is not too small
                widget.setFont(QFont("Arial", font_size))

        event.accept()

    def show_element_details(self, symbol):
        """Shows detailed information about an element in the same window below the table."""
        name = self.elements.element_names[symbol]
        atomic_number = self.elements.get_atomic_number(symbol)
        atomic_mass = self.elements.get_atomic_mass(symbol)
        oxidation_states = self.elements.get_oxidation_states(symbol)
        electronegativity = self.elements.get_electronegativity(symbol)
        density = self.elements.get_density(symbol)
        electron_config = self.elements.get_electron_configuration(symbol)
        category = self.elements.get_element_category(symbol)

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

        self.details_label.setText(properties.strip())

    def create_search_bar(self):
        """Creates a search bar and search button."""
        search_layout = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by symbol or name")
        self.search_input.setFixedHeight(30)
        self.search_input.setFont(QFont("Arial", 12))
        self.search_input.setStyleSheet("color: white; background-color: #444;")
        self.search_input.returnPressed.connect(self.search_element)

        search_layout.addWidget(self.search_input)
        self.main_layout.addLayout(search_layout)

    def search_element(self):
        """Search for an element by its symbol or name."""
        search_term = self.search_input.text().strip().capitalize()
        symbol = self.find_element_by_symbol_or_name(search_term)
        if symbol:
            self.show_element_details(symbol)
        else:
            QMessageBox.warning(self, "Not Found", "Element not found.", QMessageBox.Ok)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_mode_manager = DarkModeManager()
    dark_mode_manager.apply_palette()  # Apply the dark mode
    window = PeriodicTableApp()
    window.show()
    sys.exit(app.exec_())
