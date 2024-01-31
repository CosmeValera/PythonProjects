import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout, QTableWidget, QTableWidgetItem
from qt_material import apply_stylesheet

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        apply_stylesheet(self, theme='gmvTheme.xml')

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 GroupBox with Table Example')
        self.setGeometry(100, 100, 400, 300)

        self.createTableGroupBox()

    def createTableGroupBox(self):
        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(10, 10, 380, 280)

        vbox = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Age', 'Country'])
        
        # Inserting sample data
        data = [('John', 30, 'USA'),
                ('Emily', 25, 'Canada'),
                ('Michael', 40, 'UK')]
        
        self.tableWidget.setRowCount(len(data))

        for i, (name, age, country) in enumerate(data):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(age)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(country))

        vbox.addWidget(self.tableWidget)
        self.groupBox.setLayout(vbox)
        # self.setCentralWidget(self.tableWidget)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
