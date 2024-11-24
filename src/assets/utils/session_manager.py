class SessionManager:
    def __init__(self):
        self.sessions = {}  # Store active sessions by user ID
        self.current_dirs = {}  # Store current working directory for each session

    def create_session(self, user_id):
        self.sessions[user_id] = True
        self.current_dirs[user_id] = "/"

    def end_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]
            del self.current_dirs[user_id]

    def has_active_session(self, user_id):
        return user_id in self.sessions

    def get_current_dir(self, user_id):
        return self.current_dirs.get(user_id, "/")

    def set_current_dir(self, user_id, new_dir):
        self.current_dirs[user_id] = new_dir 