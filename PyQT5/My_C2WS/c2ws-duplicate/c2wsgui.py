import sys
import os
from PyQt5.QtWidgets import QApplication
from gui import Controller
from classes import User
from handlers import ConfigHandler

def main():
    config = ConfigHandler()
    config.load_messages()
    config.read_minipc_config()

    user = "YourMockUser"  # Provide a mock username
    user_sessions = []  # Provide mock user sessions if needed

    user_class = User(user, sessions=user_sessions)
    c = Controller(config, user_class)

    sys.exit(c.run())

if __name__ == '__main__':
    main()
