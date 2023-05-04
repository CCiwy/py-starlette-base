from src.services.base import BaseService



def hash_password(password):
    # todo: implement this
    return password

def create_token():
    return 'asdf'


class UserModel:
    # todo: create this as Basemodel instance
    def __init__(self, name, password):
        self.name = name
        self.salted_pass = hash_password(password)
        self.token = False # delete after implementing as BaseModel


    def start_session(self):
        self.token = create_token()
        # add expiration timer
        return self.token

class UserService(BaseService):
    instance_name = 'user'
    users = dict()


    def verifiy_password(self, user: UserModel, password: str) -> bool:
        hashed = hash_password(password)
        return hashed == user.salted_pass


    def get_user(self, user_name):
        return self.users.get(user_name, False)



    def create_user(self, user_name, password):
        self.users[user_name] = UserModel(user_name, password)


