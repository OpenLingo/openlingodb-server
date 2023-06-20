from typing import List
from devfu.db import Database


def get_all_notes() -> List[dict]:
    sql = """
           SELECT 
               n.id, 
               n.user_id, 
               n.`comment`, 
               n.json_data, 
               n.entity, 
               n.entity_id, 
               n.is_public
               
           FROM note AS n
        """

    with Database() as db:
        return db.query_list(sql)


def get_note(note_id: int) -> dict:
    sql = """
        SELECT 
            n.id, 
            n.user_id, 
            n.`comment`, 
            n.json_data, 
            n.entity, 
            n.entity_id, 
            n.is_public
            
        FROM note AS n
        WHERE id=:note_id
        """

    with Database() as db:
        return db.query_one(sql, note_id=note_id)


def update_note(note: dict):
    for nullable in ['json_data', 'entity', 'entity_id', 'is_public']:
        note[nullable] = note[nullable] if nullable in note and \
                                           (note[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE note
        SET  
            user_id=:user_id, 
            `comment`=:comment, 
            json_data=:json_data, 
            entity=:entity, 
            entity_id=:entity_id, 
            is_public=:is_public
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **note)


def insert_note(note: dict) -> int:
    for nullable in ['json_data', 'entity', 'entity_id', 'is_public']:
        note[nullable] = note[nullable] if nullable in note and \
                                           (note[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO note(user_id,`comment`,json_data,entity,entity_id,is_public)
        VALUES (:user_id,:comment,:json_data,:entity,:entity_id,:is_public)
    """

    with Database() as db:
        db.execute(sql, **note)
        return db.last_id()


def patch_note(note_id: int, data: dict):
    patchable_fields = ['user_id', 'comment', 'json_data', 'entity', 'entity_id', 'is_public']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `note` SET {} WHERE id=:note_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, note_id=note_id, **data)


def delete_note(note_id: int):
    sql = """
        DELETE FROM note 
        WHERE id=:note_id
    """

    with Database() as db:
        db.execute(sql, note_id=note_id)


def note_exists(note_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `note` WHERE id=:note_id);"

    with Database() as db:
        return db.scalar(sql, note_id=note_id) != 0

