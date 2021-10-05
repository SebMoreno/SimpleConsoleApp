import json


class DataBase:
    users = []

    def __init__(self, users=None):
        self.load_users()
        if users is not None:
            self.users = users

    def load_users(self):
        with open("data/usuarios.txt", "r") as f:
            users_json = f.read().split(";\n")[:-1]
        self.users = [json.loads(i) for i in users_json]

    def save_users(self):
        with open("data/usuarios.txt", "w") as f:
            for u in self.users:
                f.write(json.dumps(u, indent=1) + ";\n")

    def add_user(self, new_user):
        self.users.append(new_user)
        with open("data/usuarios.txt", "a") as f:
            f.write(json.dumps(new_user, indent=1) + ";\n")

    def delete_user(self, user):
        self.users.remove(user)
        self.save_users()


users_db = DataBase()
