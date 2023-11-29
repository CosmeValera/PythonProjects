#################################################################################
# Copyright: EU Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: view.py
# Code Management Tool File Version: 03.05.00.00
# Date: 21/12/2022
# SDD component: C2WS
# Purpose: C2WS Gui view
# Implemented Requirements: Python3, NX, LDAP
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 03.01.00.00   | 18/02/2022    | GMV - GCS Cybersecurity team  | First version
# 03.02.00.00   | 22/04/2022    | GMV - GCS Cybersecurity team  | Changes in UI
# 03.05.00.00   | 21/12/2022    | GMV - GCS Cybersecurity team  | Added screen config management
# 03.06.00.01   | 30/05/2023    | GMV - GCS Cybersecurity team  | Changed message and dialog management
#################################################################################

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QGridLayout, QGroupBox, QHBoxLayout, QLineEdit, QMainWindow, QPushButton, QWidget, QTabWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QTableView, QCheckBox, QLabel, QDialog, QDialogButtonBox, QFormLayout)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from classes import Session
from functools import partial
import datetime
import socket
from config import VERSION

class QMessageBoxDialog(QMessageBox):

    def __init__(self, config_handler):
            super(QMessageBox, self).__init__()
            self.title = ""
            self.message = ""
            self.resize(1, 1)
            
            self.ch = config_handler


    def load_dialog(self, message_name, args=[], action=None):
        if type(args) == str:
            args = (args, )

        try:
            msg = self.ch.messages[message_name]
            if msg["title"] not in self.title:
                self.title += msg["title"].format(action=action)

            self.message = msg["msg"].format(*args, action=action)
            
            if msg["category"] == "critical":
                self.show_dialog_critical()
            elif msg["category"] == "information":
                self.show_dialog_information()
            elif msg["category"] == "question":
                return self.show_dialog_question()
            elif msg["category"] == "non-template":
                self.set_dialog()
            else:
                print(f'Not recognized given message category {msg["category"]}, review the message.json config file.') # TODO: Log

        except TypeError as t:
            raise Exception("Dialog args must be an iterable (tuple or list)")
        except KeyError as k:
            raise Exception(f"Given message name {message_name} not found in message.json file") # TODO: Log


    def show_dialog_critical(self):
        QMessageBox.critical(
                    self,
                    "Error - " + self.title,
                    self.message,
                    buttons=QMessageBox.Ok
                )


    def show_dialog_information(self):
        QMessageBox.information(
                    self,
                    "Information - " + self.title,
                    self.message,
                    buttons=QMessageBox.Ok
                )


    def show_dialog_question(self):
        buttonReply = QMessageBox.question(
                    self,
                    "Question - " + self.title,
                    self.message,
                    buttons=QMessageBox.Cancel | QMessageBox.Ok
                )
        return buttonReply == QMessageBox.Ok


    def set_dialog(self):
        self.setWindowTitle(self.title)
        self.setText(self.message)


class View(QMainWindow):
    connectSignal = pyqtSignal()
    connectSignalSession = pyqtSignal()
    disconnectSignal = pyqtSignal()
    terminateSignal = pyqtSignal()
    cancelSignal = pyqtSignal()
    cancelSignalSession = pyqtSignal()
    favSignal = pyqtSignal(Session)
    settingsSignal = pyqtSignal()
    applySignal = pyqtSignal()
    passwordSignal = pyqtSignal()
    disclaimerSignal = pyqtSignal() 
    checkConnectionsSignal = pyqtSignal()
    checkSignal = pyqtSignal()

    def __init__(self, model_data, config_handler, minutes_sv):
        super(QMainWindow, self).__init__()

        self.all_sessions = []
        self.last_sessions = []
        self.fav_sessions = []
        self.update_sessions = []
        self.update_data(model_data)
        self.dialogs = list()
        self.config_handler = config_handler

        self.selected_session = Session()
        self.selected_session_message = Session()
        self.last_fav_session = Session()
        self.ldap_user = model_data.get_ldap_user()

        self.minutes_sv = minutes_sv
        self.initUi()


    def initUi(self):
        # Set main window dimesions
        self.title = f"C2WS {VERSION} - Connect to Workstation"
        
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)

        self.resize(self.width, self.height)
        
        # Main panel of the window
        self.panel_widget= QWidget()

        ##############
        self.panel_widget.layout = QVBoxLayout(self.panel_widget)

        # Initialize tab screen
        self.panel_widget.tabs = QTabWidget()

        self.panel_widget.tab1 = MyTabWidget(self, self.fav_sessions)
        self.panel_widget.tab2 = MyTabWidget(self, self.last_sessions)
        self.panel_widget.tab3 = MyTabWidget(self, self.all_sessions)
        # self.panel_widget.button.set

        self.panel_widget.tabs.resize(300,200)
        
        # Add tabs
        self.panel_widget.tabs.addTab(self.panel_widget.tab1,"Favorites")
        self.panel_widget.tabs.addTab(self.panel_widget.tab2,"Last Sessions")
        self.panel_widget.tabs.addTab(self.panel_widget.tab3,"All")

        # Add tabs to widget
        self.panel_widget.layout.addWidget(self.panel_widget.tabs)
        self.panel_widget.setLayout(self.panel_widget.layout)
        ##############
        
        buttonLayout = QHBoxLayout()
        self.settingsButton = QPushButton()
        self.settingsButton.setText("Settings")
        self.checkButton = QPushButton()
        self.checkButton.setText("Check status")
        self.checkButton.hide()
        self.connectButton = QPushButton()
        self.connectButton.setText("Connect")
        buttonLayout.addWidget(self.settingsButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.checkButton)
        buttonLayout.addWidget(self.connectButton)
        self.settingsButton.clicked.connect(self.settingsSignal)
        self.checkButton.clicked.connect(self.checkSignal)
        self.connectButton.clicked.connect(self.connectSignal)
        self.panel_widget.layout.addLayout(buttonLayout)

        self.panel_widget.user_text = QLabel(self)

        self.panel_widget.user_text.setText("Connected user: " + self.ldap_user)
        self.panel_widget.user_text.setStyleSheet("border:2px solid grey; border-radius: 5px;background-color: silver;color: grey")
        
        self.panel_widget.layout.addWidget(self.panel_widget.user_text)

        self.setCentralWidget(self.panel_widget)


    def update_data(self, model_data):
        self.all_sessions = model_data.get_full_list()
        self.last_sessions = model_data.get_last_sessions_list()
        self.fav_sessions = model_data.get_fav_list()


    def update_view_data(self, model_data):
        self.update_data(model_data)
        self.panel_widget.tab1.update_tab(self.fav_sessions)
        self.panel_widget.tab2.update_tab(self.last_sessions)
        if self.panel_widget.tabs.currentIndex() != 2:
            self.panel_widget.tab3.update_tab(self.all_sessions)


    def show_connect(self, model):
        # Add list of Sessions for show 
        self.connection_widget = ConnectionWidget(self, self.selected_session, model.get_current_sessions())
        self.dialogs.append(self.connection_widget)
        self.connection_widget.show()


    def show_connection_widget(self, secs):
        self.dialogs[-1].show_connect(secs)


    def show_settings(self):
        settings = SettingsWidget(self)
        self.dialogs.append(settings)
        settings.show()


    def ask_user(self, ws):
        question_dialog = QMessageBoxDialog(self.config_handler)
        buttonReplay = question_dialog.load_dialog("ask_user", ws)
        return buttonReplay


    def close_windows_for_connection(self):
        self.connection_widget.alert_time.close()
        self.connection_widget.close()


    def cancel_window_for_connection(self):
        self.connection_widget.close()


class ConnectionWidget(QMainWindow):

    def __init__(self, view, connection_data, current_sessions):
        super(QMainWindow, self).__init__()
        self.user = connection_data.user
        self.ws = connection_data.ws
        self.view = view

        self.current_sessions = current_sessions
        self.initUi()


    def initUi(self):
        self.title = f"C2WS - {VERSION} {self.user} {self.ws}"
        self.setWindowTitle(self.title)
        
        # Set main window dimesions
        self.width = 1000
        self.height = 500
        self.resize(self.width, self.height)
        
        # Main panel of the window
        self.panel_widget= QWidget()

        ##############
        self.panel_widget.layout = QVBoxLayout(self.panel_widget)

        # Initialize tab screen

        self.table = TableConnections(self, self.view, self.current_sessions)

        self.table.resize(300,200)

        self.text_label = QLabel()
        self.text_label.setWordWrap(True)
        self.text_label.setText(self.view.config_handler.messages["list_sessions"]["msg"].format(self.ws))
        
        self.panel_widget.user_text = QLabel()
        self.panel_widget.user_text.setText(self.view.panel_widget.user_text.text())
        self.panel_widget.user_text.setStyleSheet(self.view.panel_widget.user_text.styleSheet())

        self.panel_widget.layout.addWidget(self.text_label)
        self.panel_widget.layout.addWidget(self.table)
        self.panel_widget.layout.addWidget(self.panel_widget.user_text)
        self.panel_widget.setLayout(self.panel_widget.layout)
        ##############

        self.setCentralWidget(self.panel_widget)


    def show_connect(self, secs):
        self.seconds = secs 
        self.count = self.seconds * 10

        self.alert_time = QMessageBoxDialog(self.view.config_handler)
        self.end_time = datetime.datetime.now() + datetime.timedelta(seconds=secs)

        # Determine if Disconnect or Terminate
        action = ""
        if self.view.selected_session_message.endsession.casefold() == "disconnect":
            action = "Disconnect"
        elif self.view.selected_session_message.endsession.casefold() == "terminate":
            action = "Terminate"

        timer = QTimer(self)
        timer.timeout.connect(partial(self.show_time, action))
        timer.start(self.count)
        
        self.alert_time.setStandardButtons(QMessageBox.Cancel)
        user = self.view.selected_session_message.user
        time = str(self.end_time - datetime.datetime.now())[:-7]

        
        
        self.alert_time.load_dialog("alert_time_action", (user, time), action=action)
        button = self.alert_time.exec()

        if button == QMessageBox.Cancel:
            timer.stop()

    
    def show_time(self, action):
        self.count -= 1
        
        if self.end_time <= datetime.datetime.now():
            # disconnect session and update view
            self.alert_time.close()

            sure_close = QMessageBoxDialog(self.view.config_handler)

            # Assign Disconnect or Terminate button depending on server configuration
            if action == "Disconnect":
                disconnect_button = sure_close.addButton("Disconnect", QMessageBox.ActionRole)
                disconnect_button.clicked.connect(self.view.disconnectSignal)
            elif action == "Terminate":
                terminate_button = sure_close.addButton("Terminate", QMessageBox.ActionRole)
                terminate_button.clicked.connect(self.view.terminateSignal)

            cancel_button = sure_close.addButton("Cancel", QMessageBox.ActionRole)
            cancel_button.clicked.connect(self.view.cancelSignal)

            sure_close.load_dialog("sure_close_action", action=action)
            sure_close.exec()

        elif (self.end_time - datetime.datetime.now()).seconds%30 == 0:
            self.view.checkConnectionsSignal.emit()

        user = self.view.selected_session_message.user
        time = str(self.end_time - datetime.datetime.now())[:-7]
        self.alert_time.load_dialog("alert_time_action", (user, time), action=action)


class SettingsWidget(QMainWindow):


    def __init__(self, view):
        super(QMainWindow, self).__init__()
        self.selected_session = Session()
        self.view = view
        self.initUi()

    
    def initUi(self):
        # Set main window dimesions
        self.title = f"C2WS {VERSION} - Settings"

        self.width = 500
        self.height = 160
        self.setWindowTitle(self.title)
        
        self.resize(self.width, self.height)
        
        # Main panel of the window
        self.panel_widget= QWidget()

        ##############
        self.panel_widget.layout = QVBoxLayout(self.panel_widget)

        groupbox_sv = QGroupBox("Thinclient screensaver")

        box_sv = QHBoxLayout()

        sv_label = QLabel(self)
        sv_label.setText("Screensaver lock time: ")
        sv_input = QtWidgets.QLineEdit()
        sv_input.setValidator(QIntValidator(0, 100))
        sv_input.setText(self.view.minutes_sv)
        sv_input.textChanged.connect(partial(setattr, self.view, "minutes_sv"))

        minutes_label = QLabel(self)
        minutes_label.setText("minutes")
        apply_button = QPushButton(self)
        apply_button.setText("Apply")
        apply_button.clicked.connect(self.view.applySignal)

        box_sv.addWidget(sv_label)
        box_sv.addWidget(sv_input)
        box_sv.addWidget(minutes_label)
        box_sv.addWidget(apply_button)
        

        groupbox_sv.setLayout(box_sv)

        self.panel_widget.user_text = QLabel()
        self.panel_widget.user_text.setText(self.view.panel_widget.user_text.text())
        self.panel_widget.user_text.setStyleSheet(self.view.panel_widget.user_text.styleSheet())
        self.panel_widget.user_text.setFixedHeight(self.view.panel_widget.user_text.height())

        self.panel_widget.layout.addWidget(groupbox_sv)
        self.panel_widget.layout.addWidget(self.panel_widget.user_text)
        self.panel_widget.setLayout(self.panel_widget.layout)

        self.setCentralWidget(self.panel_widget)

        
class DisclaimerWidget(QMainWindow):


    def __init__(self, view):
        super(QMainWindow, self).__init__()
        self.view = view
        self.initUi()


    def initUi(self):
        # Set main window dimesions
        self.title = self.view.config_handler.messages["disclaimer"]["title"].format(VERSION)
        
        self.width = 500
        self.height = 400
        self.setWindowTitle(self.title)
        
        self.resize(self.width, self.height)
        
        # Main panel of the window
        self.panel_widget= QWidget()
        

        ##############
        self.panel_widget.layout = QVBoxLayout(self.panel_widget)
        self.grid_panel = QGridLayout()


        self.title_label = QLabel()
        self.title_label.setText("Connect To Workstation")
        self.title_label.setStyleSheet("font-size: 26px; margin-left: 70px")
        self.grid_panel.addWidget(self.title_label, 0, 0)

        self.disclaimer_label = QLabel()
        self.disclaimer_label.setText("Disclaimer:")
        self.disclaimer_label.setStyleSheet("font-size: 24px; margin-left: 70px; margin-top: 0px")
        self.grid_panel.addWidget(self.disclaimer_label,1, 0)

        self.text_label = QLabel()
        self.text_label.setText(self.view.config_handler.messages["disclaimer"]["msg"])
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("margin-left: 70px;")
        self.grid_panel.addWidget(self.text_label,2, 0)
        group = QGroupBox()
        self.grid_panel.setHorizontalSpacing(10)
        group.setLayout(self.grid_panel)

        self.panel_widget.layout.addWidget(group)

        accept_disclaimer_button = QPushButton(self)
        accept_disclaimer_button.setText("Accept")
        accept_disclaimer_button.clicked.connect(self.view.disclaimerSignal)
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(accept_disclaimer_button)
        self.panel_widget.layout.addLayout(buttonLayout)

        self.panel_widget.user_text = QLabel()
        self.panel_widget.user_text.setText(self.view.panel_widget.user_text.text())
        self.panel_widget.user_text.setStyleSheet(self.view.panel_widget.user_text.styleSheet())
        self.panel_widget.user_text.setFixedHeight(self.view.panel_widget.user_text.height())

        self.panel_widget.layout.addWidget(self.panel_widget.user_text)

        self.panel_widget.setLayout(self.panel_widget.layout)

        self.setCentralWidget(self.panel_widget)

     
class TableConnections(QTableWidget):
    def __init__(self, connection_session_view, view, sessions):
        super(QWidget, self).__init__(connection_session_view)
        self.connection_session_view = connection_session_view
        self.layout = QVBoxLayout(self)
        self.view = view
        
        self.table = TableSessions(connection_session_view, sessions)
        self.layout.addWidget(self.table)
        
        self.buttonPanel = QWidget()
        self.buttonLayout = QHBoxLayout(self.buttonPanel)
        self.messageButton = QPushButton("Send Message")
        self.cancelButton = QPushButton("Cancel")
        self.messageButton.clicked.connect(self.view.connectSignalSession)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.messageButton)
        self.cancelButton.clicked.connect(self.view.cancelSignalSession)
        self.buttonLayout.setAlignment(Qt.AlignRight)
        self.buttonPanel.setLayout(self.buttonLayout)
        
        self.layout.addWidget(self.buttonPanel)

        self.setLayout(self.layout)
        
    def update_tab(self, new_sessions):
        self.table.update_from_list(new_sessions)


class MyTabWidget(QWidget):


    def __init__(self, view, sessions):
        super(QWidget, self).__init__(view)
        self.view = view
        self.layout = QVBoxLayout(self)
       
        self.table = MyTableWidget(view, sessions)
        self.layout.addWidget(self.table)
        
        self.setLayout(self.layout)


    def update_tab(self, new_sessions):
        self.table.update_from_list(new_sessions)


class MyTableWidget(QTableWidget):


    def __init__(self, view, sessions):
        super(QTableWidget, self).__init__(view)
        self.view = view
        self.setSelectionBehavior(QTableView.SelectRows)
        self.cellClicked.connect(partial(self.select_session, self.view))
        
        self.headers = ["Fav", "Element", "Workstation", "Protocol", "User"]
        self.setColumnCount(len(self.headers))
        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 270)
        self.setHorizontalHeaderLabels(self.headers)

        self.data = sessions
        self.set_data()


    def update_from_list(self, data_list):
        self.clearContents()
        self.data = data_list
        
        self.set_data()


    def set_data(self):
        self.setRowCount(len(self.data))
        for index, session in enumerate(self.data):
            # 0: fav
            cellPanel = QWidget()
            cellLayout = QVBoxLayout(cellPanel)
            checkBox = QCheckBox()
            checkBox.setChecked(session.fav)
            checkBox.stateChanged.connect(partial(self.view.favSignal.emit, session))
            cellLayout.addWidget(checkBox)
            cellLayout.setAlignment(Qt.AlignCenter)
            cellPanel.setLayout(cellLayout)
            self.setCellWidget(index, 0, cellPanel)

            # 1: elem
            self.setItem(index, 1, QTableWidgetItem(str(session.elem)))
            # 2: ws
            self.setItem(index, 2, QTableWidgetItem(str(session.ws)))
            # 3: prot
            self.setItem(index, 3, QTableWidgetItem(str(session.prot)))
            # 4: user
            self.setItem(index, 4, QTableWidgetItem(str(session.user)))


    def select_session(self, view):
        selected_row_index = self.selectedIndexes()[0].row()
        view.selected_session = self.data[selected_row_index]
        if view.selected_session.prot.casefold() == "nx":
            view.checkButton.show()
        else:
            view.checkButton.hide()


class TableSessions(QTableWidget):


    def __init__(self, connection_view, sessions):
        super(QTableWidget, self).__init__(connection_view)
        self.connection_view = connection_view
        self.setSelectionBehavior(QTableView.SelectRows)
        self.cellClicked.connect(partial(self.select_session, self.connection_view.view))
        self.headers = ["Element", "Workstation", "MiniPC", "Protocol", "User", "Session Id", "Date", "Status"]
        self.setColumnCount(len(self.headers))
        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 190)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 100)
        self.setColumnWidth(5, 145)
        self.setColumnWidth(6, 150)
        self.setColumnWidth(7, 100)

        self.setHorizontalHeaderLabels(self.headers)

        self.data = sessions
        self.set_data()


    def update_from_list(self, data_list):
        self.clearContents()
        self.data = data_list
        
        self.set_data()


    def set_data(self):
        self.setRowCount(len(self.data))
        for index, session in enumerate(self.data):
            try:
                minipc = socket.gethostbyaddr(session.minipc)[0]
            except:
                minipc = session.minipc
            # 0: element
            self.setItem(index, 0, QTableWidgetItem(str(session.elem)))
            # 1: workstation
            self.setItem(index, 1, QTableWidgetItem(str(session.ws)))
            # 2: minipc 
            self.setItem(index, 2, QTableWidgetItem(str(minipc)))
            # 3: protocol
            self.setItem(index, 3, QTableWidgetItem(str(session.prot)))
            # 4: user
            self.setItem(index, 4, QTableWidgetItem(str(session.user)))
            # 5: session id
            self.setItem(index, 5, QTableWidgetItem(str(session.id)))
            # 6: last connection
            self.setItem(index, 6, QTableWidgetItem(str(session.last_connection)))
            # 7: status
            self.setItem(index, 7, QTableWidgetItem(str(session.status)))


    def select_session(self, view):
        selected_row_index = self.selectedIndexes()[0].row()
        view.selected_session_message = self.data[selected_row_index]
