import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
from functools import partial
from qtawesome import icon
from qt_material import apply_stylesheet

class MyTableWidget(QTableWidget):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.cellClicked.connect(partial(self.select_session, parent))

        self.headers = ["Fav", "Element", "Workstation", "Protocol", "User"]
        self.setColumnCount(len(self.headers))
        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 270)
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

    def select_session(self, view):
        selected_row_index = self.selectedIndexes()[0].row()
        view.selected_session = self.data[selected_row_index]

class DataFilterApp(QWidget):
    def __init__(self):
        super().__init__()
        apply_stylesheet(self, theme="gmvTheme.xml")

        self.data = [
            {"fav": False, "elem": "Manzana", "ws": "WS1", "prot": "Protocol1", "user": "User1"},
            {"fav": True, "elem": "Portatil", "ws": "WS2", "prot": "UDP", "user": "User2"},
            {"fav": True, "elem": "Raqueta", "ws": "WS3", "prot": "TCPIP", "user": "Joan"},
            {"fav": False, "elem": "Granada", "ws": "WS4", "prot": "IPV24", "user": "Helena"},
        ]
        self.filtered_data = self.data.copy()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Type to filter...")
        self.filter_input.setClearButtonEnabled(True)
        search_icon = icon('fa.search', color='white')
        self.filter_input.addAction(search_icon, QLineEdit.LeadingPosition)
        self.filter_input.textChanged.connect(self.update_filter)

        self.table_widget = MyTableWidget(self, self.filtered_data)
        
        self.print_button = QPushButton("Print Selected Session", self)
        self.print_button.clicked.connect(self.print_selected_session)

        layout.addWidget(self.filter_input)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.print_button)

        self.setLayout(layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Data Filter App')
        self.show()

    def update_filter(self, text):
        self.filtered_data = [item for item in self.data if text.lower() in str(item).lower()]
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