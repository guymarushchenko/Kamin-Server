
from db_management.db_management import DBManagement
from Entities.user import User, Permission


class UserController:

    db_management = DBManagement()

    def add_new_user(self, username, password, first_name, last_name):
        user = User(user_name=username, first_name=first_name, last_name=last_name, permission=Permission.USER.value)
        user.hash_password(password)
        user_id = self.db_management.add_new_user(user)
        return user_id

    def get_user(self, username):
        user_dict = self.db_management.get_user(username)
        user = None
        if user_dict is not None:
            user = User(user_id=user_dict['_id'].binary.hex(), user_name=user_dict['user_name'], password=user_dict['password_hash'],
                        first_name=user_dict['first_name'], last_name=user_dict['last_name'],
                        permission=user_dict['permission'])
        return user

    def get_users(self):
        users_list, moderators_list = self.db_management.get_users()
        return users_list, moderators_list

    def change_user_permission(self, user, permission):
        user.set_permission(permission)
        result = self.db_management.change_user_permission(user, permission)
        return result
