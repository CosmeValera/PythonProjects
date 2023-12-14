from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class InnerMainWindow(QMainWindow):
    def __init__(self):
        super(InnerMainWindow, self).__init__()
        self.label = QLabel("Inner Main Window")
        self.setCentralWidget(self.label)

class OuterMainWindow(QMainWindow):
    def __init__(self):
        super(OuterMainWindow, self).__init__()
        self.label = QLabel("Outer Main Window")
        self.setCentralWidget(self.label)

        # Creating and adding an instance of InnerMainWindow as a central widget
        self.inner_window = InnerMainWindow()
        self.setCentralWidget(self.inner_window)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = OuterMainWindow()
    main_window.show()
    sys.exit(app.exec_())
