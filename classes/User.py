from cryptography.fernet import Fernet
import initial.startup as startup

class User:
    def __init__(self, userID, username, password):
        self._userID = userID
        self._username = username
        self._password = password
    
    @property
    def userID(self):
        return self._userID
    
    @userID.setter
    def userID(self, value):
        if not value:
            raise ValueError("User ID cannot be empty")
        try:
            user_ID = int(value)
        except ValueError:
            raise ValueError("User ID must be an integer")
        if user_ID <= 0:
            raise ValueError("User information invalid")
        self._userID = user_ID
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if not value:
            raise ValueError("Username cannot be empty")
        if len(value) > 36:
            raise ValueError("Username cannot be longer than 36 characters")
        self._username = str(value)
    
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, value):
        if not value:
            raise ValueError("Password cannot be empty")