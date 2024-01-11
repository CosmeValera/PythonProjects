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
        
        self.headers_length = len(headers)
        self.setColumnCount(self.headers_length)
        self.setHeaderLabels(headers)
        self.addItemsRecursively(self, data)

        header = self.DraggableHeaderView(Qt.Horizontal, self)
        self.setHeader(header)

    def addItemsRecursively(self, parent, items):
        for item in items:
            currentItem = QTreeWidgetItem(parent, item[:self.headers_length])
            if len(item) > self.headers_length:
                self.addItemsRecursively(currentItem, item[self.headers_length])

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
    base_data = [
        {'Fav': 'False', 'Name': '1', 'Life': '1', 'Branch': 'Surgery'},
        {'Fav': 'False', 'Name': '2', 'Life': '1', 'Branch': 'Tree'},
        {'Fav': 'True', 'Name': '3', 'Life': '2', 'Branch': 'Surgery'},
        {'Fav': 'True', 'Name': '4', 'Life': '2', 'Branch': 'Tree'},
    ]
    base_headers = ['Fav', 'Name', 'Life', 'Branch']
    group_headers = [''] + base_headers
    
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout(self.central_widget)

        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_2 = QHBoxLayout()

        self.tag_bar = TagBar(self.update_tree_table)
        self.tree_table = EmptyTable(self.base_data, self.base_headers)

        self.horizontal_layout_1.addWidget(self.tag_bar)
        self.horizontal_layout_2.addWidget(self.tree_table)

        self.vertical_layout.addLayout(self.horizontal_layout_1)
        self.vertical_layout.addLayout(self.horizontal_layout_2)

        self.setWindowTitle('Tagbar')
        self.resize(750, 400)

    def update_tree_table(self, tags):
        if tags:
            self.createTreeTableGrouping(tags)
        else:
            self.createEmptyTable()
    
    def createEmptyTable(self):
        self.horizontal_layout_2.removeWidget(self.tree_table)
        self.tree_table = EmptyTable(self.base_data, self.base_headers)
        self.horizontal_layout_2.addWidget(self.tree_table)


    # tag_value = 'Fav' / 'Name'
    # main_line_value = 'False' / '1'
    def createTreeTableGrouping(self, tags):
        data = []
        for tag in tags:
            tag_value = tag.children()[1].text()

            distinct_values = set(item[tag_value] for item in self.base_data)
            #1
            main_lines = [(f"{tag_value}={value}",) + ('',) * len(self.base_headers) for value in distinct_values]


            # Generate sub-lines
            for main_line in main_lines:
                print("Main_line", main_line)
                sub_lines = []
                main_line_value = main_line[0].split('=')[1]
                # print(main_line_value, tag_value, main_line_value == tag_value)

                for item in self.base_data:
                    if item[tag_value] == main_line_value:
                        sub_lines.append([('',) + tuple(str(item[header]) for header in self.base_headers)])

                data.append((*main_line, [item for sub_line in sub_lines for item in sub_line]))
                print("Sublines:", sub_lines)

        self.horizontal_layout_2.removeWidget(self.tree_table)
        self.tree_table = TreeTableGrouping(data, self.group_headers)
        self.horizontal_layout_2.addWidget(self.tree_table)
        print("data: ", data)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
