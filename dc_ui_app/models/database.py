

class Database:
    def __init__(self, name, description):
        self.name = name
        self.descripton = description
        self.table_count = 0

    def set_table_count(self, table_count):
        self.table_count = table_count
