import mariadb
from typing import List
# if __name__ == '__main__':
#     DATABASE_CREDENTIALS = {  # this is only here for testing purposes.
#             'database': "openlingo",
#             'user': "root",
#             'password': "password",
#             'host': "127.0.0.1",
#             'port': 3306
#     }
# else:
#     from config import DATABASE_CREDENTIALS

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
        parameter(s): An sql query as a string.
        return(s): A list of dictionaries, each of which represents one row of the executed query.
        """
        columns = []
        output = []

        # Guard clause returns an empty list of dictionaries if sql statement
        # contains dangerous keywords
        if 'INSERT' in sql or 'UPDATE' in sql or 'DELETE' in sql:
            return [{}]
        try:
            self.cur.execute(sql, sql_args)
        except mariadb.Error as e:
            print(f"Error: {e}. The query could not be completed.")

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

    def insert(self, sql: str, sql_args: tuple):
        try:
            self.cur.execute(sql, sql_args)
        except mariadb.Error as e:
            print(f"error: {e}. Cancelling transaction.")
            self.conn.rollback()

    def update(self, sql: str, sql_args: tuple):
        try:
            self.cur.execute(sql, sql_args)
        except mariadb.Error as e:
            print(f"error: {e}. Cancelling transaction.")
            self.conn.rollback()

    def delete(self, sql: str):
        pass


# Tests
if __name__ == '__main__':
    def query_test():
        test_queries = [
            {'sql': """
                        SELECT lang.title as `language`, COUNT(lev.id) as levels 
                        FROM `language` as lang, `level` as lev
                        WHERE lang.id = lev.language_id
                        GROUP BY lang.title
                        ORDER BY COUNT(lev.id) DESC;
                    """,
             'args': (),
             'expected_outcome': 'Succeed'},
            {'sql': """
                        SELECT n.word, COUNT(nt.to_noun_id) as translations
                        FROM noun as n, noun_translation as nt
                        WHERE n.id = nt.from_noun_id
                        AND nt.to_noun_id IN (SELECT id 
                                              FROM noun
                                              WHERE language_id = ?
                                             )
                        GROUP BY n.word
                        ORDER BY COUNT(nt.to_noun_id) DESC;
                    """,
             'args': (2,),
             'expected_outcome': 'Succeed'},
            {'sql': """
                        UPDATE noun
                        SET language_id = ?,
                            level_id = ?,
                            gender = ?,
                            word = ?
                        WHERE id = ?
                    """,
             'args': (1, 1, 'm', 'jeff', 1),
             'expected_outcome': 'Fail'}
        ]
        outcomes = []
        with Database() as db:
            for query in test_queries:
                try:
                    db.query(query['sql'], query['args'])

                except:
                    print("The query function broke with these inputs:")
                    print(f"query: {query['sql']}")
                    print(f"arguments: {query['args']}")
                    break
            else:
                print('All test queries successful')
    query_test()
