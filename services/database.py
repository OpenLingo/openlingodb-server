import mariadb

from typing import List

# from config import DATABASE_CREDENTIALS
DATABASE_CREDENTIALS = {  # this is only here for testing purposes.
        'database': "openlingo",
        'user': "root",
        'password': "password",
        'host': "127.0.0.1",
        'port': 3306
}


class Database:
    def __init__(self):
        self.conn = mariadb.connect(
            database=DATABASE_CREDENTIALS['database'],
            user=DATABASE_CREDENTIALS['user'],
            password=DATABASE_CREDENTIALS['password'],
            host=DATABASE_CREDENTIALS['host'],
            port=DATABASE_CREDENTIALS['port']
        )
        self.conn.autocommit = False
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exctype, excinst, exctb):
        self.conn.close()

    def query(self, sql: str) -> List[dict]:
        """
        parameter(s): An sql query as a string.
        return(s): A list of dictionaries, each of which represents one row of the executed query.
        """
        output = []
        columns = []

        self.cur.execute(sql)

        # Retrieves column names of the query output
        for column in self.cur.description:
            columns.append(column[0])
        for row in self.cur:
            # Uses list comprehension to generate a dictionary for a given row in a query
            output.append({columns[index]: row[index] for index in range(len(columns))})
        return output
        # One-liner version of the part of this function that creates lists of dictionaries.
        # Removes the need for the output variable, but is a bit of a hassle to read.
        # return [{columns[index]: row[index] for index in range(len(columns))} for row in self.cur]

    def insert(self, sql: str):
        pass

    def update(self, sql: str):
        pass

    def delete(self, sql: str):
        pass
