import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QTreeWidget, QTreeWidgetItem, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap

class EmptyTable(QTableWidget):
    def __init__(self, data, headers):
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

class TreeTableGrouping(QTreeWidget):
    def __init__(self, data, headers):
        super().__init__()
        
        self.setColumnCount(len(headers))
        self.setHeaderLabels(headers)
        self.addItemsRecursively(self, data)

        header = self.DraggableHeaderView(Qt.Horizontal, self)
        self.setHeader(header)

    def addItemsRecursively(self, parent, items):
        for item in items:
            currentItem = QTreeWidgetItem(parent, item[:3])
            if len(item) > 3:
                self.addItemsRecursively(currentItem, item[3])

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
    def __init__(self, tree_table_callback):
        super().__init__()
        self.setAcceptDrops(True)
        self.tags = []
        self.h_layout = QHBoxLayout(self)
        self.tree_table_callback = tree_table_callback

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

        self.tree_table_callback(self.tags)

    def remove_tag(self, text):
        for tag in self.tags:
            if tag.children()[1].text() == text:
                self.h_layout.removeWidget(tag)
                tag.deleteLater()
                self.tags.remove(tag)
                break

        self.tree_table_callback(self.tags)

        #Print  :)       
        print(f'Removed tag. Now there are {len(self.tags)} tags.')
        for tag in self.tags:
            print(tag.children()[1].text())
            print(self.tags)


class MainWindow(QMainWindow):
    emptyData = [
        {'Fav': False, 'Name': 1},
        {'Fav': False, 'Name': 2},
        {'Fav': True, 'Name': 3},
        {'Fav': True, 'Name': 4},
    ]
    emptyHeaders = ['Fav', 'Name']
    
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout(self.central_widget)

        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_2 = QHBoxLayout()

        self.tag_bar = TagBar(self.update_tree_table)
        self.tree_table = EmptyTable(self.emptyData, self.emptyHeaders)

        self.horizontal_layout_1.addWidget(self.tag_bar)
        self.horizontal_layout_2.addWidget(self.tree_table)

        self.vertical_layout.addLayout(self.horizontal_layout_1)
        self.vertical_layout.addLayout(self.horizontal_layout_2)

    def update_tree_table(self, tags):
        if tags:
            self.createTreeTableGrouping(tags)
        else:
            self.createEmptyTable()
    
    def createEmptyTable(self):
        self.horizontal_layout_2.removeWidget(self.tree_table)
        self.tree_table = EmptyTable(self.emptyData, self.emptyHeaders)
        self.horizontal_layout_2.addWidget(self.tree_table)

    def createTreeTableGrouping(self, tags):
        headers = ['Group by', 'Fav', 'Name']
        
        data = []
        if any((tag.children()[1].text() == "Fav") for tag in tags) and any((tag.children()[1].text() == "Name") for tag in tags):
            data = [
                ('Fav=false', '', '', 
                    [('Name=1', '', '',
                        [('', 'false', '1')]),
                    ('Name=2', '', '',
                        [('', 'false', '2')])]),
                ('Fav=true', '', '', 
                    [('Name=3', '', '',
                        [('', 'true', '3')]),
                    ('Name=4', '', '',
                        [('', 'true', '4')])]),
            ]
        elif any((tag.children()[1].text() == "Fav") for tag in tags):
            data = [
                ('Fav=false', '', '', 
                    [('', 'false', '1'),
                    ('', 'false', '2')]),
                ('Fav=true', '', '', 
                    [('', 'true', '3'),
                    ('', 'true', '4')]),
            ]
        elif any((tag.children()[1].text() == "Name") for tag in tags):
            data = [
                ('Name=1', '', '',
                    [('', 'false', '1')]),
                ('Name=2', '', '',
                    [('', 'false', '2')]),
                ('Name=3', '', '',
                    [('', 'true', '3')]),
                ('Name=4', '', '',
                    [('', 'true', '4')]),
            ]

        self.horizontal_layout_2.removeWidget(self.tree_table)
        self.tree_table = TreeTableGrouping(data, headers)
        self.horizontal_layout_2.addWidget(self.tree_table)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
