from STRINGS import *
class UserFlags:
    request_file_path = ""
    action = NO_ACTION
    db_name = ""
    table_name = ""
    parameter = ""

    def set_request_file_path(self, path):
        self.request_file_path = path

    def get_request_file_path(self):
        return self.request_file_path

    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action


    def set_db_name(self, name):
        self.db_name = name

    def get_db_name(self):
        return self.db_name

    def set_table_name(self, name):
        self.table_name = name

    def get_table_name(self):
        return self.table_name

    def set_parameter(self, parameter):
        self.parameter = parameter

    def get_parameter(self):
        return self.parameter