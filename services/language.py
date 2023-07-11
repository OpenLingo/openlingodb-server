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


def get_all_languages() -> List[dict]:
    sql = """
               SELECT *
               FROM language
              """
    # the cursor execution and list conversion of the cur object should be handled in
    # the context manager mentioned above in order to reduce code repetition.
    cur.execute(sql)
    return [{"id": language_id,
             "code": code,
             "title": title,
             "is_gendered": bool(is_gendered)} for (language_id, code, title, is_gendered) in cur]


def get_language(language_id: int) -> dict:
    sql = """
        SELECT 
            l.id, 
            l.`code`, 
            l.title, 
            l.is_gendered
            
        FROM `language` AS l
        WHERE id=:language_id
        """

    with Database() as db:
        return db.query_one(sql, language_id=language_id)


def update_language(language: dict):
    for nullable in ['is_gendered']:
        language[nullable] = language[nullable] if nullable in language and \
                                           (language[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE `language`
        SET  
            `code`=:code, 
            title=:title, 
            is_gendered=:is_gendered
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **language)


def insert_language(language: dict) -> int:
    for nullable in ['is_gendered']:
        language[nullable] = language[nullable] if nullable in language and \
                                           (language[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO `language`(`code`,title,is_gendered)
        VALUES (:code,:title,:is_gendered)
    """

    with Database() as db:
        db.execute(sql, **language)
        return db.last_id()


def patch_language(language_id: int, data: dict):
    patchable_fields = ['code', 'title', 'is_gendered']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `language` SET {} WHERE id=:language_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, language_id=language_id, **data)


def delete_language(language_id: int):
    sql = """
        DELETE FROM language 
        WHERE id=:language_id
    """

    with Database() as db:
        db.execute(sql, language_id=language_id)


def language_exists(language_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `language` WHERE id=:language_id);"

    with Database() as db:
        return db.scalar(sql, language_id=language_id) != 0

