import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QTreeWidget, QTreeWidgetItem, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QFrame, QSizePolicy, QLineEdit
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from qt_material import apply_stylesheet

class EmptyTable(QTableWidget):
    def __init__(self, data, headers):
        super().__init__()
        apply_stylesheet(self, theme='gmvTheme.xml')

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
        apply_stylesheet(self, theme='gmvTheme.xml')
        
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
        apply_stylesheet(self, theme='gmvTheme.xml')
        self.setAcceptDrops(True)
        self.tags = []
        self.h_layout = QHBoxLayout(self)
        self.tree_table_callback = tree_table_callback

        # Create an invisible tag as a placeholder
        self.add_invisible_tag()

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        text = event.mimeData().text()
        self.add_tag_to_bar(text)
        event.accept()

    def add_tag_to_bar(self, text):
        tag = QWidget()
        tag.setStyleSheet("QWidget {background-color: #191919; border-radius: 14px;}")
        
        hbox = QHBoxLayout()
        hbox.setContentsMargins(4, 4, 4, 4)

        tag_label = QLabel(text)
        tag_label.setStyleSheet('margin-left: 6px; border: 0px; padding: 0;')

        close_button = QPushButton('✕')
        close_button.setFixedSize(16, 16)
        close_button.clicked.connect(lambda: self.remove_tag(text))
        close_button.setStyleSheet("border: 0px; padding: 0; margin: 0px 6px 0px 0px; color: #999999;")

        hbox.addWidget(tag_label)
        hbox.addWidget(close_button)
        tag.setLayout(hbox)

        self.h_layout.insertWidget(len(self.tags), tag)  # Insert the new tag before the invisible tag
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

        # Print  :)       
        print(f'Removed tag. Now there are {len(self.tags)} tags.')
        for tag in self.tags:
            print(tag.children()[1].text())

        # Re-add the invisible tag to the end
        self.add_invisible_tag()

    def add_invisible_tag(self):
        invisible_tag = QWidget()
        invisible_tag.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.h_layout.addWidget(invisible_tag)

    def dragMoveEvent(self, event):
        event.accept()


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
        apply_stylesheet(self, theme='gmvTheme.xml')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout(self.central_widget)

        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_2 = QHBoxLayout()

        self.tag_bar = TagBar(self.update_tree_table)
        self.tree_table = EmptyTable(self.base_data, self.base_headers)

        self.horizontal_layout_1.addWidget(self.tag_bar, 1)
        self.horizontal_layout_1.addWidget(QLabel(), 1)
        self.horizontal_layout_2.addWidget(self.tree_table)

        self.vertical_layout.addLayout(self.horizontal_layout_1)
        self.vertical_layout.addLayout(self.horizontal_layout_2)

        self.setWindowTitle('Tagbar')
        self.resize(750, 400)

        initial_tag_value = 'Fav'
        self.tag_bar.add_tag_to_bar(initial_tag_value)

    def update_tree_table(self, tags):
        if tags:
            self.createTreeTableGrouping(tags)
        else:
            self.createEmptyTable()
    
    def createEmptyTable(self):
        self.horizontal_layout_2.removeWidget(self.tree_table)
        self.tree_table = EmptyTable(self.base_data, self.base_headers)
        self.horizontal_layout_2.addWidget(self.tree_table)


    # current_tag = 'Fav' / 'Name'; main_line_value = 'False' / '1'
    def createTreeTableGrouping(self, tags):
        self.result_data = []
        self.createGroupedData(0, tags, self.base_data)

        self.horizontal_layout_2.removeWidget(self.tree_table)
        self.tree_table = TreeTableGrouping(self.result_data, self.group_headers)
        self.horizontal_layout_2.addWidget(self.tree_table)
    
    def createGroupedData(self, level, tags, data, all_sub_lines=[]):
        if level < len(tags):
            tag = tags[level]
            current_tag = tag.children()[1].text() # current_tag -> 'Fav' / 'Name'
            
            # Get distinct values from the filtered data
            distinct_values = set(row[current_tag] for row in data)
            
            for value in distinct_values: # value -> 'True' / '1'
                main_line = (f"{current_tag}={value}",) + ('',) * len(self.base_headers)
                
                filtered_data = [row for row in data if row[current_tag] == value]

                # Recursive call with filtered_data
                self.createGroupedData(level + 1, tags, filtered_data, all_sub_lines)
                
                # Append data based on the level
                self.result_data.append((*main_line, [row for sub_line in all_sub_lines for row in sub_line]))

                all_sub_lines.clear()

        else:
            # Calculate sub_lines only at the last level
            for row in data:
                all_sub_lines.append([('',) + tuple(str(row[header]) for header in self.base_headers)])

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
