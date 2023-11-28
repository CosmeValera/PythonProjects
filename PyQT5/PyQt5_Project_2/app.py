from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

# Following this: https://www.youtube.com/watch?v=MOItX2aKTGc
def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 200, 300)
    window.setWindowTitle("My simple GUI")

    layout = QVBoxLayout()

    label = QLabel("Press the button below")
    button = QPushButton("Press me !")
    
    label.setText("Press the button below")
    label.setFont(QFont("Arial", 16))
    label.move(50,100)

    button.clicked.connect(on_clicked)

    layout.addWidget(label)
    layout.addWidget(button)

    window.show()
    app.exec_()

def on_clicked():
    print("Hello world")

if __name__ == '__main__':
    main()