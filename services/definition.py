from typing import List
from devfu.db import Database


def get_all_definitions(noun_id: int) -> List[dict]:
    sql = """
           SELECT 
               dn.id, 
               dt.title, 
               dn.noun_id, 
               dn.`text`
               
           FROM definition AS dn, dialect AS dt
           WHERE dn.noun_id = :noun_id
        """

    with Database() as db:
        return db.query_list(sql, noun_id=noun_id)


def get_definitions(noun_id: int) -> List[dict]:
    sql = """
        SELECT 
            d.id, 
            d.dialect_id, 
            d.noun_id, 
            d.`text`
        FROM definition AS d
        WHERE d.noun_id = :noun_id
        AND d.dialect_id = 1 -- Limits the definitions to those with an australian english dialect. Remove later!
        ORDER BY d.dialect_id
        """

    with Database() as db:
        return db.query_list(sql, noun_id=noun_id)


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
        INSERT INTO definition(dialect_id, noun_id, `text`)
        VALUES (:dialect_id, :noun_id, :text)
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

