from circles_local_database_python.to_sql_interface import ToSQLInterface


class Point(ToSQLInterface):
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def to_sql(self):
        return f"POINT ({self.longitude}, {self.latitude})"
