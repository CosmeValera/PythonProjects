# WE ARE NOT DOING THIS; we use TreeWidget and grouping all by the first column

import sys
from PyQt5.QtWidgets import QApplication, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem


app = QApplication(sys.argv)

model = QStandardItemModel()
model.setHorizontalHeaderLabels(['Item', 'Value'])

rootItem = model.invisibleRootItem()

item1 = QStandardItem('Item 1')
item1.appendRow([QStandardItem('Child 1'), QStandardItem('Child Value 1')])
item1.appendRow([QStandardItem('Child 2'), QStandardItem('Child Value 2')])

item2 = QStandardItem('Item 2')
item2.appendRow([QStandardItem('Child 3'), QStandardItem('Child Value 3')])

rootItem.appendRow([item1, QStandardItem('Value 1')])
rootItem.appendRow([item2, QStandardItem('Value 2')])

treeView = QTreeView()
treeView.setModel(model)
treeView.setHeaderHidden(True)  # Hide headers
treeView.show()

sys.exit(app.exec_())
