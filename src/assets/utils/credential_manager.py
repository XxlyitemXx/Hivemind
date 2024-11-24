import json
import os
import bcrypt
from typing import Optional

class CredentialManager:
    def __init__(self, register_key):
        self.register_key = register_key
        self.cred_file = "credentials.json"
        self._load_credentials()

    def _load_credentials(self):
        if not os.path.exists(self.cred_file):
            self._save_credentials({})
        
        with open(self.cred_file, 'r') as f:
            self.credentials = json.load(f)

    def _save_credentials(self, creds):
        with open(self.cred_file, 'w') as f:
            json.dump(creds, f, indent=4)

    def register_user(self, username: str, password: str, reg_key: str) -> bool:
        if reg_key != self.register_key:
            return False, "Invalid registration key"
            
        if username in self.credentials:
            return False, "Username already exists"
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        self.credentials[username] = hashed.decode('utf-8')
        self._save_credentials(self.credentials)
        return True, "Registration successful"

    def verify_credentials(self, username: str, password: str) -> bool:
        if username not in self.credentials:
            return False
        
        stored_hash = self.credentials[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)