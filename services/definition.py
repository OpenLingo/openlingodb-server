from typing import List
from devfu.db import Database


def get_all_definitions() -> List[dict]:
    sql = """
           SELECT 
               d.id, 
               d.dialect_id, 
               d.noun_id, 
               d.`text`
               
           FROM definition AS d
        """

    with Database() as db:
        return db.query_list(sql)


def get_definition(definition_id: int) -> dict:
    sql = """
        SELECT 
            d.id, 
            d.dialect_id, 
            d.noun_id, 
            d.`text`
            
        FROM definition AS d
        WHERE id=:definition_id
        """

    with Database() as db:
        return db.query_one(sql, definition_id=definition_id)


def update_definition(definition: dict):
    sql = """
        UPDATE definition
        SET  
            dialect_id=:dialect_id, 
            noun_id=:noun_id, 
            `text`=:text
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **definition)


def insert_definition(definition: dict) -> int:
    sql = """
        INSERT INTO definition(dialect_id,noun_id,`text`)
        VALUES (:dialect_id,:noun_id,:text)
    """

    with Database() as db:
        db.execute(sql, **definition)
        return db.last_id()


def patch_definition(definition_id: int, data: dict):
    patchable_fields = ['dialect_id', 'noun_id', 'text']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `definition` SET {} WHERE id=:definition_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, definition_id=definition_id, **data)


def delete_definition(definition_id: int):
    sql = """
        DELETE FROM definition 
        WHERE id=:definition_id
    """

    with Database() as db:
        db.execute(sql, definition_id=definition_id)


def definition_exists(definition_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `definition` WHERE id=:definition_id);"

    with Database() as db:
        return db.scalar(sql, definition_id=definition_id) != 0

