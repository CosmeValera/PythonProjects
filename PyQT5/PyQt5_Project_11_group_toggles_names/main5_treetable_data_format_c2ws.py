import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self, data):
        super().__init__()

        self.data = data

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['Workspace', 'Session'])

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree_widget)

        self.populate_tree(self.data, self.tree_widget.invisibleRootItem())

        self.tree_widget.itemClicked.connect(self.item_clicked)

    def populate_tree(self, data, parent_item):
        for item_data in data:
            fav = item_data['fav']
            sessions = item_data['sessions']

            item = QTreeWidgetItem(parent_item, [f'Favorite: {fav}'])

            for session_data in sessions:
                ws = session_data['ws']
                session_item = QTreeWidgetItem(item, [f'Workspace: {ws}'])

                for session in session_data['sessions']:
                    session_object = session['session']
                    session_item.addChild(QTreeWidgetItem(session_item, [f'Session: {session_object}']))

    def item_clicked(self, item, column):
        if item.childCount() == 0:  # Leaf item (session)
            session_value = item.text(column).split(': ')[1]
            print(session_value)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    data = [
        {'fav': True, 'sessions': [{'ws': 'csim-ws-1.int.gcc1.gal', 'sessions': [{'session': "<classes.Session object at 0x7f720574ff60>"}]},
                                    {'ws': 'csim-ws-2.int.gcc1.gal', 'sessions': [{'session': "<classes.Session object at 0x7f7205761048>"}]}]},
        {'fav': False, 'sessions': [{'ws': 'csim-ws-1.int.gcc1.gal', 'sessions': [{'session': "<classes.Session object at 0x7f720574ff98>"}]},
                                     {'ws': 'csim-ws-2.int.gcc1.gal', 'sessions': [{'session': "<classes.Session object at 0x7f7205761080>"}]}]}
    ]

    window = MainWindow(data)
    window.setGeometry(100, 100, 800, 600)
    window.show()

    sys.exit(app.exec_())
