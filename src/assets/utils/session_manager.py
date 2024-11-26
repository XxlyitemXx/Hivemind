class SessionManager:
    def __init__(self):
        self.sessions = {}  # Store active sessions by user ID
        self.current_dirs = {}  # Store current working directory for each session
        self.venv_active = {}  # Store active venv for each session
        self._default_dir = self._get_default_directory()

    def _get_default_directory(self):
        """Get the appropriate default directory based on OS"""
        import os
        import platform
        
        system = platform.system()
        if system == "Windows":
            return os.path.expanduser("~")  # Returns C:\Users\username
        else:  # Linux/Unix/MacOS
            return os.path.expanduser("~")  # Returns /home/username

    def create_session(self, user_id):
        self.sessions[user_id] = True
        self.current_dirs[user_id] = self._default_dir
        self.venv_active[user_id] = False

    def end_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]
            del self.current_dirs[user_id]
            del self.venv_active[user_id]

    def has_active_session(self, user_id):
        return user_id in self.sessions

    def get_current_dir(self, user_id):
        return self.current_dirs.get(user_id, "/")

    def set_current_dir(self, user_id, new_dir):
        self.current_dirs[user_id] = new_dir 

    def activate_venv(self, user_id, venv_path):
        self.venv_active[user_id] = venv_path

    def deactivate_venv(self, user_id):
        self.venv_active[user_id] = False

    def is_venv_active(self, user_id):
        return self.venv_active.get(user_id, False)