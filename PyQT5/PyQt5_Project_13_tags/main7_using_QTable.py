import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap

class NormalTable(QTableWidget):
    def __init__(self, headers, data):
        super().__init__()

        self.headers = headers
        self.data = data

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setRowCount(len(self.data))

        self.populateTable()

        header = self.DraggableHeaderView(Qt.Horizontal, self)
        self.setHorizontalHeader(header)

    def populateTable(self):
        for row, rowData in enumerate(self.data):
            for col, key in enumerate(self.headers):
                item = QTableWidgetItem(str(rowData[key]))
                if key == "Fav":
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Checked if rowData[key] else Qt.Unchecked)
                self.setItem(row, col, item)

    class DraggableHeaderView(QHeaderView):
        def __init__(self, orientation, parent):
            super().__init__(orientation, parent)

        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                index = self.logicalIndexAt(event.pos())
                if index != -1:
                    item_text = self.model().headerData(index, self.orientation())
                    drag = QDrag(self)
                    mime_data = QMimeData()
                    mime_data.setText(item_text)
                    drag.setMimeData(mime_data)
                    drag.exec_(Qt.MoveAction)

class TagBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.tags = []
        self.h_layout = QHBoxLayout(self)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        print('Something was dropped in the TagBar')
        text = event.mimeData().text()
        self.add_tag_to_bar(text)
        event.accept()

    def add_tag_to_bar(self, text):
        tag = QFrame()
        tag.setStyleSheet('border:1px solid rgb(192, 192, 192); border-radius: 4px;')
        tag.setContentsMargins(2, 2, 2, 2)
        tag.setFixedHeight(28)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(4, 4, 4, 4)
        tag_label = QLabel(text)
        hbox.addWidget(tag_label)
        close_button = QPushButton('x')
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(lambda: self.remove_tag(text))
        hbox.addWidget(close_button)
        tag.setLayout(hbox)
        self.h_layout.addWidget(tag)
        self.tags.append(tag)

    def remove_tag(self, text):
        for tag in self.tags:
            if tag.children()[1].text() == text:
                self.h_layout.removeWidget(tag)
                tag.deleteLater()
                self.tags.remove(tag)
                break

        # Print  :)       
        print(f'Removed tag. Now there are {len(self.tags)} tags.')
        for tag in self.tags:
            print(tag.children()[1].text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout(self.central_widget)

        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_2 = QHBoxLayout()

        self.tag_bar = TagBar()

        headers = ["Fav", "Element", "Workstation", "Protocol", "User"]
        data = [
            {"Fav": False, "Element": "Caja", "Workstation": "WS1", "Protocol": "IPV48", "User": "Bohe"},
            {"Fav": False, "Element": "Manzana", "Workstation": "WS2", "Protocol": "Protocol1", "User": "User1"},
            {"Fav": True, "Element": "Portatil", "Workstation": "WS3", "Protocol": "UDP", "User": "User2"},
            {"Fav": False, "Element": "Raqueta", "Workstation": "WS4", "Protocol": "TCPIP", "User": "Joan"},
            {"Fav": True, "Element": "Granada", "Workstation": "WS5", "Protocol": "IPV24", "User": "Helena"},
        ]

        self.tree_table = NormalTable(headers, data)

        self.horizontal_layout_1.addWidget(self.tag_bar)
        self.horizontal_layout_2.addWidget(self.tree_table)

        self.vertical_layout.addLayout(self.horizontal_layout_1)
        self.vertical_layout.addLayout(self.horizontal_layout_2)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
