from typing import List
from devfu.db import Database


def get_all_dialects() -> List[dict]:
    sql = """
           SELECT 
               d.id, 
               d.language_id, 
               d.`code`, 
               d.title
               
           FROM dialect AS d
        """

    with Database() as db:
        return db.query_list(sql)


def get_dialect(dialect_id: int) -> dict:
    sql = """
        SELECT 
            d.id, 
            d.language_id, 
            d.`code`, 
            d.title
            
        FROM dialect AS d
        WHERE id=:dialect_id
        """

    with Database() as db:
        return db.query_one(sql, dialect_id=dialect_id)


def update_dialect(dialect: dict):
    sql = """
        UPDATE dialect
        SET  
            language_id=:language_id, 
            `code`=:code, 
            title=:title
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **dialect)


def insert_dialect(dialect: dict) -> int:
    sql = """
        INSERT INTO dialect(language_id,`code`,title)
        VALUES (:language_id,:code,:title)
    """

    with Database() as db:
        db.execute(sql, **dialect)
        return db.last_id()


def patch_dialect(dialect_id: int, data: dict):
    patchable_fields = ['language_id', 'code', 'title']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `dialect` SET {} WHERE id=:dialect_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, dialect_id=dialect_id, **data)


def delete_dialect(dialect_id: int):
    sql = """
        DELETE FROM dialect 
        WHERE id=:dialect_id
    """

    with Database() as db:
        db.execute(sql, dialect_id=dialect_id)


def dialect_exists(dialect_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `dialect` WHERE id=:dialect_id);"

    with Database() as db:
        return db.scalar(sql, dialect_id=dialect_id) != 0

