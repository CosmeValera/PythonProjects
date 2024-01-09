import sys
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QFrame
from functools import partial

class TagBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tag Bar')
        self.tags = []
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(4)
        self.setLayout(self.h_layout)
        self.line_edit = QLineEdit()
        self.line_edit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setContentsMargins(2,2,2,2)
        self.h_layout.setContentsMargins(2,2,2,2)
        self.refresh()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.line_edit.returnPressed.connect(self.create_tags)

    def create_tags(self):
        new_tags = self.line_edit.text().split(', ')
        print(new_tags)
        self.line_edit.setText('')
        self.tags.extend(new_tags)
        self.tags = list(set(self.tags))
        self.tags.sort(key=lambda x: x.lower())
        self.refresh()

    def refresh(self):
        for i in reversed(range(self.h_layout.count())):
            self.h_layout.itemAt(i).widget().setParent(None)
        for tag in self.tags:
            self.add_tag_to_bar(tag)
        self.h_layout.addWidget(self.line_edit)
        self.line_edit.setFocus()

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
        close_button.clicked.connect(partial(self.remove_tag, text))
        hbox.addWidget(close_button)
        tag.setLayout(hbox)
        self.h_layout.addWidget(tag)

    def remove_tag(self, text):
        self.tags.remove(text)
        self.refresh()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TagBar()
    sys.exit(app.exec_())
