from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from qtawesome import icon

def main():
    app = QApplication([])

    data = [
        ('1', 'Category 1', [('1.1', 'Item 1.1')]),
        ('2', 'Category 2', [('2.1', 'Item 2.1'), ('2.2', 'Item 2.2')]),
    ]

    tree = QTreeWidget()
    tree.setHeaderLabels(['Id', 'Name'])
    tree.header().setDefaultAlignment(Qt.AlignLeft)

    header_flag = True  # Set this flag as per your requirement
    fa_arrow = 'fa.arrow-down' if header_flag else 'fa.arrow-up'
    arrow_icon = icon(fa_arrow, color='#999999')

    tree.headerItem().setIcon(0, arrow_icon)
    tree.headerItem().setIcon(1, arrow_icon)

    for id_, name, items in data:
        parent = QTreeWidgetItem([id_, name])
        tree.addTopLevelItem(parent)
        for sub_id, sub_name in items:
            QTreeWidgetItem(parent, [sub_id, sub_name])

    tree.show()
    app.exec_()

if __name__ == '__main__':
    main()