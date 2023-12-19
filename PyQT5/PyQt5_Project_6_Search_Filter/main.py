import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget,
QTableWidgetItem, QPushButton, QSpacerItem, QSizePolicy, QShortcut, QLabel, QStackedWidget, QFrame,
QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtSvg import QSvgWidget
from functools import partial
from qtawesome import icon
from qt_material import apply_stylesheet
from guiStyles import FILTER_STYLES, SIDEBAR_STYLES, SIDEBAR_BUTTON_STYLES, SEPARATOR_STYLES

# MY PROJECT
class MyTableWidget(QTableWidget):
    FIRST_COLUMN_WIDTH = 70
    CHECKBOX_SIZE = 20

    def __init__(self, parent, data):
        super().__init__(parent)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.cellClicked.connect(partial(self.select_session, parent))
        self.verticalHeader().sectionClicked.connect(self.row_header_clicked)
        self.horizontalHeader().sectionClicked.connect(self.header_clicked)
        self.itemSelectionChanged.connect(self.selection_changed)

        self.headers = ["Fav", "Element", "Workstation", "Protocol", "User"]
        self.setColumnCount(len(self.headers))
        self.setColumnWidth(0, self.FIRST_COLUMN_WIDTH)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 140)
        self.setColumnWidth(3, 120)
        self.setColumnWidth(4, 80)
        self.setHorizontalHeaderLabels(self.headers)

        self.fav_sort_order = None
        self.elem_sort_order = None
        self.ws_sort_order = None
        self.prot_sort_order = None
        self.user_sort_order = None

        self.data = data
        self.set_data()
        
    def update_from_list(self, data_list):
        self.clearContents()
        self.data = data_list
        self.set_data()

    def set_data(self):
        self.setRowCount(len(self.data))
        for index, session in enumerate(self.data):
            # 0 fav
            checkBox = QCheckBox()
            checkBox.setChecked(session.get("fav"))

            checkbox_padding = self.FIRST_COLUMN_WIDTH // 2 - self.CHECKBOX_SIZE // 2
            checkBox.setStyleSheet(f"QCheckBox {{ padding-left: {checkbox_padding}px; }}")

            self.setCellWidget(index, 0, checkBox)
            self.setItem(index, 0, QTableWidgetItem())
            self.setItem(index, 1, QTableWidgetItem(str(session.get("elem"))))
            self.setItem(index, 2, QTableWidgetItem(str(session.get("ws"))))
            self.setItem(index, 3, QTableWidgetItem(str(session.get("prot"))))
            self.setItem(index, 4, QTableWidgetItem(str(session.get("user"))))
            
            # Set items as read-only
            for col in range(self.columnCount()):
                item = self.item(index, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            
            self.highligh_fav_rows(index, session)
            self.highligh_default_rows(index, session)

    def highligh_fav_rows(self, index, session):
        if session.get("fav") is True:
            for col in range(self.columnCount()):
                item = self.item(index, col)
                if item:
                    item.setBackground(QColor(223, 0, 36, 26))
                    # item.setForeground(QColor())

    def highligh_default_rows(self, index, session):
        if session.get("user") is "User1":
            for col in range(self.columnCount()):
                item = self.item(index, col)
                if item:
                    item.setBackground(QColor(246, 246, 246, 26))
                    # item.setForeground(QColor())

    def select_session(self, view):
        selected_row_index = self.selectedIndexes()[0].row()
        view.selected_session = self.data[selected_row_index]

    def selection_changed(self):
        selected_items = self.selectedItems()
        if not selected_items:
            self.parent().selected_session = None

    def row_header_clicked(self, selected_row_index):
        self.parent().selected_session = self.data[selected_row_index]

    def header_clicked(self, index):
        column_names = ["fav", "elem", "ws", "prot", "user"]

        if index or index == 0:
            self.toggle_order_by(column_names[index])
            self.set_data()
        
    def toggle_order_by(self, header):
        header_flag = getattr(self, header + "_sort_order")

        if header_flag is None or header_flag == Qt.AscendingOrder:
            self.data.sort(key=lambda x: x.get(header), reverse=True)
            setattr(self, header + '_sort_order', Qt.DescendingOrder)
        else:
            self.data.sort(key=lambda x: x.get(header))
            setattr(self, header + '_sort_order', Qt.AscendingOrder)


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

class SidebarWidget(QWidget):
    # Each option has 2 buttons: Icon and Icon + text
    def __init__(self, buttons_icon, buttons_text):
        super().__init__()
        self.separator_styles = SEPARATOR_STYLES
        self.buttons_icon = buttons_icon
        self.buttons_text = buttons_text
        self.layout = QVBoxLayout(self)
        self.initUi()

    def initUi(self):
        self.insertLogo()
        self.insertSeparator()
        self.insertButtons()
        self.layout.addStretch()
        self.setLayout(self.layout)

    def insertLogo(self):
        logo_container = QWidget()
        logo_layout = QHBoxLayout()
        logo_svg = QSvgWidget('logo.svg')
        logo_svg.setFixedSize(38, 14)
        logo_layout.addWidget(logo_svg)
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_container.setLayout(logo_layout)

        self.layout.addWidget(logo_container)

    def insertSeparator(self):
        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        line_separator.setStyleSheet(self.separator_styles)

        self.layout.addWidget(line_separator)

    def insertButtons(self):
        for button_icon, button_text in zip(self.buttons_icon, self.buttons_text):
            self.layout.addWidget(button_icon)
            self.layout.addWidget(button_text)

    def enterEvent(self, event):
        for button_text in self.buttons_text:
            button_text.setVisible(True)
        for button_icon in self.buttons_icon:
            button_icon.setVisible(False)

    def leaveEvent(self, event):
        for button_text in self.buttons_text:
            button_text.setVisible(False)
        for button_icon in self.buttons_icon:
            button_icon.setVisible(True)

class DataFilterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.filter_styles = FILTER_STYLES
        self.sidebar_styles = SIDEBAR_STYLES
        self.sidebar_button_styles = SIDEBAR_BUTTON_STYLES
        apply_stylesheet(self, theme="gmvTheme.xml")

        self.ldap_user = "system"
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
        ### Page layout ###
        self.layout = QHBoxLayout()
        self.layout_content = QVBoxLayout()

        self.stacked_widget = QStackedWidget()
        self.home_widget = HomeWidget(self)
        self.settings_widget = SettingsWidget(self)

        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.settings_widget)
        ### END: Page layout ###

        ### Filter layout ###
        # Create a horizontal layout to organize the spacer, filter_input, and user_connection_layout
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setContentsMargins(0, 5, 15, 5)

        # New user info layout
        user_connection_layout = QVBoxLayout()
        user_connection_layout.setSpacing(2)

        # Create a label for the user icon
        user_icon = QLabel()
        user_icon.setPixmap(icon('fa.user', color='#999999').pixmap(24, 24))
        # Set border-radius only for the user_icon
        user_icon.setStyleSheet("QLabel { border-radius: 14px; border: 2px solid #999999; }")

        user_label = QLabel(self.ldap_user)
        user_label.setStyleSheet("QLabel { color:#BBBBBB; font-weight: bold; font-size: 8pt;}")

        # Add user icon and label to the user_connection_layout
        user_connection_layout.addWidget(user_icon, alignment=Qt.AlignCenter)
        user_connection_layout.addWidget(user_label, alignment=Qt.AlignCenter)
        ### END: Filter layout ###


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
        self.buttons_emoji = []
        self.buttons_text = []
        self.create_menu_button("C2WS", "🏠", 0)
        self.create_menu_button("Settings", "⚙️", 1)

        self.hoverable_menu = SidebarWidget(self.buttons_emoji, self.buttons_text)
        self.hoverable_menu.setAttribute(Qt.WA_StyledBackground, True)
        self.hoverable_menu.setStyleSheet(self.sidebar_styles)
        ### END: MENU ###

        ### PRINT ###
        self.print_button = QPushButton("Print Selected Session", self)
        self.print_button.clicked.connect(self.print_selected_session)
        ### END: PRINT ###

        ### Add layout ###
        self.filter_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding))
        self.filter_layout.addWidget(filter_input)
        self.filter_layout.addItem(QSpacerItem(10, 0, QSizePolicy.Fixed))
        self.filter_layout.addLayout(user_connection_layout)

        self.layout_content.addLayout(self.filter_layout)
        self.layout_content.addWidget(self.stacked_widget)
        self.layout_content.addWidget(self.print_button)

        self.layout.addWidget(self.hoverable_menu)
        self.layout.addLayout(self.layout_content)

        self.setLayout(self.layout)
        ### END: Add layout ###

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Data Filter App')
        self.resize(800,400)
        self.show()

    def create_menu_button(self, text, emoji, index):
        button_emoji = QPushButton(emoji)
        button_text = QPushButton(f"{emoji} {text}")
        button_text.setVisible(False)
        button_emoji.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(index))
        button_text.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(index))
        button_emoji.setStyleSheet(self.sidebar_button_styles)
        button_text.setStyleSheet(self.sidebar_button_styles)
        self.buttons_emoji.append(button_emoji)
        self.buttons_text.append(button_text)

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
    data_filter_app = DataFilterApp()
    sys.exit(app.exec_())
