from typing import List
from devfu.db import Database


def get_all_noun_dialects() -> List[dict]:
    sql = """
           SELECT 
               nd.id, 
               nd.dialect_id, 
               nd.noun_id
               
           FROM noun_dialect AS nd
        """

    with Database() as db:
        return db.query_list(sql)


def get_noun_dialect(noun_dialect_id: int) -> dict:
    sql = """
        SELECT 
            nd.id, 
            nd.dialect_id, 
            nd.noun_id
            
        FROM noun_dialect AS nd
        WHERE id=:noun_dialect_id
        """

    with Database() as db:
        return db.query_one(sql, noun_dialect_id=noun_dialect_id)


def update_noun_dialect(noun_dialect: dict):
    sql = """
        UPDATE noun_dialect
        SET  
            dialect_id=:dialect_id, 
            noun_id=:noun_id
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **noun_dialect)


def insert_noun_dialect(noun_dialect: dict) -> int:
    sql = """
        INSERT INTO noun_dialect(dialect_id,noun_id)
        VALUES (:dialect_id,:noun_id)
    """

    with Database() as db:
        db.execute(sql, **noun_dialect)
        return db.last_id()


def patch_noun_dialect(noun_dialect_id: int, data: dict):
    patchable_fields = ['dialect_id', 'noun_id']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `noun_dialect` SET {} WHERE id=:noun_dialect_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, noun_dialect_id=noun_dialect_id, **data)


def delete_noun_dialect(noun_dialect_id: int):
    sql = """
        DELETE FROM noun_dialect 
        WHERE id=:noun_dialect_id
    """

    with Database() as db:
        db.execute(sql, noun_dialect_id=noun_dialect_id)


def noun_dialect_exists(noun_dialect_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `noun_dialect` WHERE id=:noun_dialect_id);"

    with Database() as db:
        return db.scalar(sql, noun_dialect_id=noun_dialect_id) != 0

