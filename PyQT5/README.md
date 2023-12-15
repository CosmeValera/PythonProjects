## C2WS image
![](img/previous_C2WS.png)

## 🚀 Getting Started
To initiate a PyQt5 project, the initial steps involve installing PyQt5, PyQt5-tools, and PyInstaller. 
```bash
pip install pyqt5
pip install pyqt5-tools
pip install pyinstaller
```

## 🎨 Adding Qt Material Theme
```bash
pip install qt-material
```
```python
# [Other imports]
from qt_material import apply_stylesheet

class GUI(QMainWindow):
    def __init__(self):
        # [Code]
        apply_stylesheet(app, theme='light_teal.xml')  # Choose the theme you prefer

if __name__ == '__main__':
    # [Main code]
```


## 💻 Setting up Qt Designer

1. **Download Qt Designer:**
   Download Qt Designer from [this link](https://build-system.fman.io/qt-designer-download).

2. **Open Qt Designer:**
   After downloading, open Qt Designer.

3. **Create Your Project:**
   - In Qt Designer, create your graphical user interface (GUI) by adding widgets and arranging them as desired.
   - Save your project file (e.g., `gui_app.ui`) in the same folder as your Python script (`app.py`).

## 📄 Creating the Python Script

1. **Create `app.py`:**
   Create a Python script (e.g., `app.py`) in the same folder as your project.

2. **Add Code to `app.py`:**
   Use the following code as a starting point for your `app.py`:

   ```python
   import sys
   from PyQt5 import uic
   from PyQt5.QtWidgets import QMainWindow, QApplication

   class PyQt5_Project_1(QMainWindow):
       def __init__(self):
           super().__init__()
           uic.loadUi("gui_app.ui", self)

   if __name__ == '__main__':
       app = QApplication(sys.argv)
       GUI = PyQt5_Project_1()
       GUI.show()
       sys.exit(app.exec())
    ```
## 🏃 Running Your PyQt5 Project
1. **Run the Python Script:**
Open a terminal in the project folder and run the following command:
```bash
python app.py
```
This command will execute your PyQt5 application, and you should see the GUI you designed in Qt Designer.


##### PyQt5_Project_6_Search_Filter is the main project