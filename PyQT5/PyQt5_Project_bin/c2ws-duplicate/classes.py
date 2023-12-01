import datetime


class Session:
    
    def __init__(self, fav=False, user="", ws="", elem="", prot="", endsession="", max_sessions=4, date="", status="", minipc="", lc=""):
        self.id = ""
        self.fav = fav
        self.user = user
        self.ws = ws
        self.elem = elem
        self.prot = prot
        self.endsession = endsession
        self.max_sessions = max_sessions
        self.date = date
        self.status = status
        self.minipc = minipc
        self.last_connection = lc


    def set_id(self, id_value):
        self.id = id_value


    def get_id(self):
        return self.id


    def toggle_fav(self):
        self.fav = not(self.fav)


    def update_date(self):
        self.date = datetime.datetime.now()


class User:
    
    def __init__(self, name="", groupKillNoMachineSessions="", sessions = []):
        self.name = name
        self.groupKillNoMachineSessions = groupKillNoMachineSessions
        self.sessions = sessions
