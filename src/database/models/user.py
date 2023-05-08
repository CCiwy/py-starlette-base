# Import Built-Ins
from datetime import datetime
from enum import Enum, auto


# Import Third-Party
from sqlalchemy import Column
from sqlalchemy import String, DateTime, Integer

# Import Home-Grown
from src.database.basemodel import BaseModel


from src.utils.uuid import get_uuid
from src.utils.auth import generate_auth_token

# DEFINE CONSTANTS
MAX_LEN_USERNAME = 16
MAX_LEN_PASSWORD = 16 # maybe add minlen too
TOKEN_LEN = 128


def hash_password(password):
    """ not yet implemented """
    return password

class UserModel(BaseModel):
    
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(MAX_LEN_USERNAME), nullable=False)
    
    salted_pass = Column(String(MAX_LEN_PASSWORD))
    token = Column(String(TOKEN_LEN))
    
    creation_time = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    uuid = Column(String(36), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.salted_pass = hash_password(password)
        self.token = ''
    
        self.uuid = get_uuid(name)



    def verifiy_password(self, password: str) -> bool:
        hashed = hash_password(password)
        return hashed == self.salted_pass


    def start_session(self):
        self.token = generate_auth_token(self.uuid)
        # add expiration timer
        return self.token
