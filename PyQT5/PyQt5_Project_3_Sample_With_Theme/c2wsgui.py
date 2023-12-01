import sys
from PyQt5.QtWidgets import QApplication

from model import MyModel
from view import MyView
from controller import MyController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize Model, View, and Controller
    model = MyModel()
    view = MyView()
    controller = MyController(model, view)

    # Set up connections between Model, View, and Controller
    view.update_view(model.get_data())

    # Show the GUI
    view.show()

    sys.exit(app.exec_())
