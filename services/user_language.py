from typing import List
from devfu.db import Database


def get_all_user_languages() -> List[dict]:
    sql = """
           SELECT 
               ul.id, 
               ul.dialect_id, 
               ul.level_id, 
               ul.user_id, 
               ul.is_native, 
               ul.qual_level
               
           FROM user_language AS ul
        """

    with Database() as db:
        return db.query_list(sql)


def get_user_language(user_language_id: int) -> dict:
    sql = """
        SELECT 
            ul.id, 
            ul.dialect_id, 
            ul.level_id, 
            ul.user_id, 
            ul.is_native, 
            ul.qual_level
            
        FROM user_language AS ul
        WHERE id=:user_language_id
        """

    with Database() as db:
        return db.query_one(sql, user_language_id=user_language_id)


def update_user_language(user_language: dict):
    for nullable in ['level_id']:
        user_language[nullable] = user_language[nullable] if nullable in user_language and \
                                           (user_language[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE user_language
        SET  
            dialect_id=:dialect_id, 
            level_id=:level_id, 
            user_id=:user_id, 
            is_native=:is_native, 
            qual_level=:qual_level
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **user_language)


def insert_user_language(user_language: dict) -> int:
    for nullable in ['level_id']:
        user_language[nullable] = user_language[nullable] if nullable in user_language and \
                                           (user_language[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO user_language(dialect_id,level_id,user_id,is_native,qual_level)
        VALUES (:dialect_id,:level_id,:user_id,:is_native,:qual_level)
    """

    with Database() as db:
        db.execute(sql, **user_language)
        return db.last_id()


def patch_user_language(user_language_id: int, data: dict):
    patchable_fields = ['dialect_id', 'level_id', 'user_id', 'is_native', 'qual_level']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `user_language` SET {} WHERE id=:user_language_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, user_language_id=user_language_id, **data)


def delete_user_language(user_language_id: int):
    sql = """
        DELETE FROM user_language 
        WHERE id=:user_language_id
    """

    with Database() as db:
        db.execute(sql, user_language_id=user_language_id)


def user_language_exists(user_language_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `user_language` WHERE id=:user_language_id);"

    with Database() as db:
        return db.scalar(sql, user_language_id=user_language_id) != 0

