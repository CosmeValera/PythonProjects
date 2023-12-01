from PyQt5.QtWidgets import QApplication
from gui.view import DisclaimerWidget
from model import Model
from view import View, QMessageBoxDialog
from handlers.nomachine_handler import NoMachineHandler
from handlers import Logger

logger = Logger("c2ws")

class Controller:

    def __init__(self, config, user):
        self._model = Model()
        self._model.set_user(user)
        self._model.create_user_ldap_folder()
        self._model.set_or_load_sessions(self.generate_elements(config))
        logger.log("GAL.GCS.GCSS.C2WS.USER_SESSIONS_CREATED")
        
        self._view = View(self._model, config, self.get_minutes_sv())
        self._disc = DisclaimerWidget(self._view)
        self.config_handler = config
        self.assign_signals()

    def assign_signals(self):
        # Your signal connections go here...

    def get_minutes_sv(self):
        # Your existing method for getting minutes_sv...

    def cancel_connected_sessions(self):
        # Your existing method...

    def check_session(self):
        # Your existing method...

    def disconnect_user_connect(self):
        # Your existing method...

    def terminate_user_connect(self):
        # Your existing method...

    def cancel_user_connect(self):
        logger.log("GAL.GCS.GCSS.C2WS.USER_PRESS", ("cancel",))

    def check_sessions_left(self):
        # Your existing method...

    def apply_sv_connect(self):
        # Your existing method...

    def on_connection_click_connect(self):
        # Your existing method...

    def on_click_settings_connect(self):
        self._view.show_settings()

    def on_click_connect(self):
        ses_id = self._view.selected_session.get_id()
        self._model.update_date_session_with_id(ses_id)
        self._view.update_view_data(self._model)
        if self._view.selected_session.user == "":
            critical_dialog = QMessageBoxDialog(self.config_handler)
            critical_dialog.load_dialog("no_session_selected")
        else:
            if "default_wks" in self.config_handler.thinclient_info.keys():
                default_ws = self.config_handler.thinclient_info["default_wks"]
                if self._view.selected_session.ws != default_ws:
                    logger.log("GAL.GCS.GCSS.C2WS.NON_DEFAULT_WKS_SELECTED")
                    warning_dialog = QMessageBoxDialog(self.config_handler)
                    buttonReplyOk = warning_dialog.load_dialog("no_ws_default", default_ws)
                    if not buttonReplyOk:
                        return
                self.open_new_nomachine(self._view.selected_session.ws, self._view.selected_session.user, self._view.selected_session.max_sessions)
            else:
                logger.log("GAL.GCS.GCSS.C2WS.ERROR_CONFIG_FILE", ("default_wks", "Thinclient"))
                error_dialog = QMessageBoxDialog(self.config_handler)
                error_dialog.load_dialog("error_in_config_file", ("default_wks", "Thinclient"))

    def open_new_nomachine(self, ws, user, max_sessions):
        # Your existing method...

    def show_not_available_sessions(self, current_sessions):
        # Your existing method...

    def on_click_fav(self, session):
        ses_id = session.get_id()
        self._model.set_fav_session_with_id(ses_id)
        self._view.update_view_data(self._model)

    def run_view(self):
        self._disc.close()
        self._view.show()

    def run(self):
        self._disc.show()
        return self._app.exec_()
    
    def generate_elements(self, config):
        # Your existing method...

