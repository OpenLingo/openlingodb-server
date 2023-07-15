import mariadb
import sys

from typing import List
from devfu.db import Database

# would be best to implement this is a class to make use of a context manager
try:
    conn = mariadb.connect(
        # these credentials should be put in config.py
        database="openlingo",
        user="root",
        password="password",
        host="127.0.0.1",
        port=3306
    )
except mariadb.Error as e:
    print(f"Error connecting to mariaDB platform: {e}")
    sys.exit(1)
cur = conn.cursor()


def get_all_nouns() -> List[dict]:
    sql = """
           SELECT n.id, n.word, n.gender, l.title
           FROM noun as n, language as l
           WHERE n.language_id = l.id
          """
    # the cursor execution and list conversion of the cur object should be handled in
    # the context manager mentioned above in order to reduce code repetition.
    cur.execute(sql)
    return [{"id": noun_id,
             "word": word,
             "gender": gender,
             "language": language} for (noun_id, word, gender, language) in cur]


def get_noun_by_id(noun_id) -> List[dict]:
    sql = """
            SELECT * FROM noun WHERE id = ?
          """
    cur.execute(sql, (noun_id,))
    return [{"id": noun_id,
             "language_id": language_id,
             "level_id": level_id,
             "gender": gender,
             "word": word} for (noun_id, language_id, level_id, gender, word) in cur]


def update_noun(noun: dict):
    sql = """
            UPDATE noun
            SET language_id = ?,
                level_id = ?,
                gender = ?,
                word = ?
            WHERE id = ?
          """
    cur.execute(sql, (noun['language_id'], noun['level_id'], noun['gender'], noun['word'], noun['id']))
    conn.commit()


def get_noun(noun_id: int) -> dict:
    sql = """
        SELECT 
            n.id, 
            n.language_id, 
            n.level_id, 
            n.gender, 
            n.word
            
        FROM noun AS n
        WHERE id=:noun_id
        """

    with Database() as db:
        return db.query_one(sql, noun_id=noun_id)


# def update_noun(noun: dict):
#     for nullable in ['level_id', 'gender']:
#         noun[nullable] = noun[nullable] if nullable in noun and \
#                                            (noun[nullable] or not nullable.endswith('_id')) else None
#
#     sql = """
#         UPDATE noun
#         SET
#             language_id=:language_id,
#             level_id=:level_id,
#             gender=:gender,
#             word=:word
#         WHERE id=:id
#     """
#
#     with Database() as db:
#         db.execute(sql, **noun)
#

def insert_noun(noun: dict) -> int:
    for nullable in ['level_id', 'gender']:
        noun[nullable] = noun[nullable] if nullable in noun and \
                                           (noun[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO noun(language_id,level_id,gender,word)
        VALUES (:language_id,:level_id,:gender,:word)
    """

    with Database() as db:
        db.execute(sql, **noun)
        return db.last_id()


def patch_noun(noun_id: int, data: dict):
    patchable_fields = ['language_id', 'level_id', 'gender', 'word']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `noun` SET {} WHERE id=:noun_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, noun_id=noun_id, **data)


def delete_noun(noun_id: int):
    sql = """
        DELETE FROM noun 
        WHERE id=:noun_id
    """

    with Database() as db:
        db.execute(sql, noun_id=noun_id)


def noun_exists(noun_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `noun` WHERE id=:noun_id);"

    with Database() as db:
        return db.scalar(sql, noun_id=noun_id) != 0

