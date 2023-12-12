import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QSpacerItem, QSizePolicy, QShortcut, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from functools import partial
from qtawesome import icon
from qt_material import apply_stylesheet
from guiStyles import FILTER_STYLES

class HomeWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.table_widget = MyTableWidget(self, parent.filtered_data)
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)

class SettingsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("Settings works!")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

# MY PROJECT
class MyTableWidget(QTableWidget):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.cellClicked.connect(partial(self.select_session, parent))
        self.verticalHeader().sectionClicked.connect(self.row_header_clicked)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.headers = ["Fav", "Element", "Workstation", "Protocol", "User"]
        self.setColumnCount(len(self.headers))
        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 140)
        self.setColumnWidth(3, 120)
        self.setColumnWidth(4, 80)
        self.setHorizontalHeaderLabels(self.headers)

        self.data = data
        self.set_data()
        
    def update_from_list(self, data_list):
        self.clearContents()
        self.data = data_list
        self.set_data()

    def set_data(self):
        self.setRowCount(len(self.data))
        for index, session in enumerate(self.data):
            # Display data in table (modify as needed)
            self.setItem(index, 0, QTableWidgetItem(str(session.get("fav", ""))))
            self.setItem(index, 1, QTableWidgetItem(str(session.get("elem", ""))))
            self.setItem(index, 2, QTableWidgetItem(str(session.get("ws", ""))))
            self.setItem(index, 3, QTableWidgetItem(str(session.get("prot", ""))))
            self.setItem(index, 4, QTableWidgetItem(str(session.get("user", ""))))
            
            # Set items as read-only
            for col in range(self.columnCount()):
                item = self.item(index, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            
            # Highlight fav rows
            if session.get("fav") is True:
                for col in range(self.columnCount()):
                    item = self.item(index, col)
                    if item:
                        item.setBackground(QColor(40, 0, 8))  # Yellow background
                        # item.setForeground(QColor())  # Yellow background
            # Highlight default row (User1)
            if session.get("user") is "User1":
                for col in range(self.columnCount()):
                    item = self.item(index, col)
                    if item:
                        item.setBackground(QColor(8, 40, 8))  # Yellow background
                        # item.setForeground(QColor())  # Yellow background

    def select_session(self, view):
        selected_row_index = self.selectedIndexes()[0].row()
        view.selected_session = self.data[selected_row_index]

    def row_header_clicked(self, selected_row_index):
        self.parent().selected_session = self.data[selected_row_index]

    def selection_changed(self):
        selected_items = self.selectedItems()
        if not selected_items:
            self.parent().selected_session = None

class DataFilterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.filter_styles = FILTER_STYLES
        apply_stylesheet(self, theme="gmvTheme.xml")

        self.data = [
            {"fav": False, "elem": "Caja", "ws": "WS1", "prot": "IPV48", "user": "Bohe"},
            {"fav": False, "elem": "Manzana", "ws": "WS2", "prot": "Protocol1", "user": "User1"},
            {"fav": True, "elem": "Portatil", "ws": "WS3", "prot": "UDP", "user": "User2"},
            {"fav": False, "elem": "Raqueta", "ws": "WS4", "prot": "TCPIP", "user": "Joan"},
            {"fav": True, "elem": "Granada", "ws": "WS5", "prot": "IPV24", "user": "Helena"},
        ]
        self.filtered_data = self.data.copy()

        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.home_widget = HomeWidget(self)
        self.settings_widget = SettingsWidget(self)

        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.settings_widget)

        self.layout = QHBoxLayout()
        self.layout_content = QVBoxLayout()

        ### LAYOUT ###
        # Create a horizontal layout to organize the filter_input and spacer
        self.filter_layout = QHBoxLayout()

        # Add a spacer on the left side to fill the space
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.filter_layout.addItem(spacer)
        ### END: LAYOUT ###

        ### FILTER ###
        filter_input = QLineEdit(self)
        filter_input.setPlaceholderText("Search...")
        filter_input.setClearButtonEnabled(True)
        filter_input.setToolTip("You can also use Ctrl + F to search")
        search_icon = icon('fa.search', color='white')
        filter_input.addAction(search_icon, QLineEdit.LeadingPosition)
        filter_input.textChanged.connect(self.update_filter)
        filter_input.setStyleSheet(self.filter_styles)

        # Placeholder style
        palette = filter_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(255, 255, 255, 90))
        filter_input.setPalette(palette)

        # Shortcut
        shortcut = QShortcut("Ctrl+F", self)
        shortcut.activated.connect(lambda: self.setFocusOnFilterInput(filter_input))
        ### END: FILTER ###

        ### MENU ###
        self.menu_layout = QVBoxLayout()
        self.menu_layout.addWidget(self.create_menu_button("Home", 0))
        self.menu_layout.addWidget(self.create_menu_button("Settings", 1))
        ### END: MENU ###

        ### TABLE ###
        # self.table_widget = MyTableWidget(self, self.filtered_data)
        ### END: TABLE ###
        
        ### PRINT ###
        self.print_button = QPushButton("Print Selected Session", self)
        self.print_button.clicked.connect(self.print_selected_session)
        ### END: PRINT ###

        ### Add layout ###
        self.layout.addLayout(self.menu_layout)
        self.filter_layout.addWidget(filter_input)
        self.layout_content.addLayout(self.filter_layout)
        self.layout_content.addWidget(self.stacked_widget)
        # self.layout_content.addWidget(self.table_widget)
        self.layout_content.addWidget(self.print_button)
        self.layout.addLayout(self.layout_content)
        ### Add layout ###

        self.setLayout(self.layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Data Filter App')
        self.resize(700,400)
        self.show()

    def create_menu_button(self, text, index):
        button = QPushButton(text, self)
        button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(index))
        return button

    def setFocusOnFilterInput(self, filter_input):
        self.table_widget.clearSelection()  # Clear table selection
        filter_input.setFocus()

    def update_filter(self, text):
        def contains_filter_text(value):
            return text.lower() in str(value).lower()
        self.filtered_data = [item for item in self.data if any(contains_filter_text(value) for value in item.values())]
        self.table_widget.update_from_list(self.filtered_data)
    
    def print_selected_session(self):
        if hasattr(self, 'selected_session'):
            print(self.selected_session)
        else:
            print("No session selected.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    DataFilterApp()
    sys.exit(app.exec_())
