from werkzeug.security import check_password_hash

class User:
    def __init__(self, email, first_name, last_name, password, has_permission):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.has_permission = has_permission

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def check_permission(self):
        return self.has_permission

    def check_password(self, password_not_hashed):
        return check_password_hash(self.password, password_not_hashed)
