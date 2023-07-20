import mariadb

from config import DATABASE_CREDENTIALS
from typing import List


class Database:
    def __init__(self):
        self.conn = mariadb.connect(
            database=DATABASE_CREDENTIALS['database'],
            user=DATABASE_CREDENTIALS['user'],
            password=DATABASE_CREDENTIALS['password'],
            host=DATABASE_CREDENTIALS['host'],
            port=DATABASE_CREDENTIALS['port']
        )

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exctype, excinst, exctb):
        try:
            self.conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}. Rolling back changes.")
            self.conn.rollback()
        finally:
            self.conn.close()

    def query(self, sql: str, sql_args: tuple = ()) -> List[dict]:
        """
        Parameter(s):
                sql (mandatory) -> An sql query as a string.
            sql_args (optional) -> a tuple containing any arguments to be parsed with
                                   the sql query, in the order that they appear in the
                                   query.
        Return(s):
                         output -> A list of dictionaries, each of which represents one
                                   row of the executed query.
        """
        columns = []
        output = []

        # Guard clause returns an empty list of dictionaries if sql statement contains
        # dangerous keywords.
        if 'INSERT' in sql or 'UPDATE' in sql or 'DELETE' in sql:
            print("Query contained dangerous keywords.")
            return [{}]
        try:
            self.cur.execute(sql, sql_args)
        except mariadb.Error as e:
            print(f"Error: {e}. The query could not be completed.")

        for column in self.cur.description:
            columns.append(column[0])  # 1st element of this dictionary is the column's name.
        for row in self.cur:
            # List comprehension generates a dictionary for a given row in a query.
            output.append({columns[index]: row[index] for index in range(len(columns))})
        return output
        # One-liner version of the part of this function that creates lists of dictionaries.
        # Removes the need for the output variable, but is a bit of a hassle to read.
        # return [{columns[index]: row[index] for index in range(len(columns))} for row in self.cur]

    def insert(self, sql: str, sql_args: tuple):
        """
        Parameter(s):
                sql (mandatory) -> An sql query as a string.
            sql_args (optional) -> a tuple containing any arguments to be parsed with
                                   the sql query, in the order that they appear in the
                                   query.
        Return(s): None
        """
        try:
            self.cur.execute(sql, sql_args)
        except mariadb.Error as e:
            print(f"error: {e}. Cancelling transaction.")
            self.conn.rollback()

    def update(self, sql: str, sql_args: tuple):
        """
        Parameter(s):
                sql (mandatory) -> An sql query as a string.
            sql_args (optional) -> a tuple containing any arguments to be parsed with
                                   the sql query, in the order that they appear in the
                                   query.
        Return(s): None
        """
        try:
            self.cur.execute(sql, sql_args)
        except mariadb.Error as e:
            print(f"error: {e}. Cancelling transaction.")
            self.conn.rollback()

    def delete(self, sql: str):
        pass
