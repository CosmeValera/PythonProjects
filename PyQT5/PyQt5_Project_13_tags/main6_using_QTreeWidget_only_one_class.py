import sys
from PyQt5.QtWidgets import QApplication, QHeaderView, QTreeWidget, QTreeWidgetItem, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap

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

class TreeTable(QTreeWidget):
    def __init__(self):
        super().__init__()
        data = [
            ('1', 'Category 1', [('1.1', 'Item 1.1', [('1.1.1', 'Subitem 1.1.1')])]),
            ('2', 'Category 2', [('2.1', 'Item 2.1'), ('2.2', 'Item 2.2')]),
        ]
        headers = ['Id', 'Name']

        self.setColumnCount(len(headers))
        self.setHeaderLabels(headers)
        self.addItemsRecursively(self, data)

        header = DraggableHeaderView(Qt.Horizontal, self)
        self.setHeader(header)

    def addItemsRecursively(self, parent, items):
        for item in items:
            currentItem = QTreeWidgetItem(parent, item[:2])
            if len(item) > 2:
                self.addItemsRecursively(currentItem, item[2])

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

        #Print  :)       
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
        self.tree_table = TreeTable()

        self.horizontal_layout_1.addWidget(self.tag_bar)
        self.horizontal_layout_2.addWidget(self.tree_table)

        self.vertical_layout.addLayout(self.horizontal_layout_1)
        self.vertical_layout.addLayout(self.horizontal_layout_2)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
