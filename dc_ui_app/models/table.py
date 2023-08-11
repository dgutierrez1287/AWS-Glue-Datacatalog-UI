

class Table:
    def __init__(self, name, description, update_time):
        self.name = name
        self.update_time = update_time
        self.description = description
        self.columns = []

    def set_column_list(self, column_list):
        self.columns = column_list

class Column:
    def __init__(self, name, col_type, comment):
        self.name = name
        self.col_type = col_type
        self.comment = comment
