from typing import List
from devfu.db import Database


def get_all_noun_translations() -> List[dict]:
    sql = """
           SELECT 
               nt.id, 
               nt.from_noun_id, 
               nt.to_noun_id, 
               nt.accuracy
               
           FROM noun_translation AS nt
        """

    with Database() as db:
        return db.query_list(sql)


def get_noun_translations(noun_id: int) -> List[dict]:
    sql = """
        SELECT id, word
        FROM noun
        WHERE id != :noun_id
        AND id IN (
            SELECT from_noun_id 
            FROM noun_translation 
            WHERE to_noun_id = :noun_id
        
            UNION
        
            SELECT to_noun_id 
            FROM noun_translation
            WHERE from_noun_id = :noun_id
        );
        """

    with Database() as db:
        return db.query_list(sql, noun_id=noun_id)


def update_noun_translation(noun_translation: dict):
    sql = """
        UPDATE noun_translation
        SET  
            from_noun_id=:from_noun_id, 
            to_noun_id=:to_noun_id, 
            accuracy=:accuracy
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **noun_translation)


def insert_noun_translation(noun_translation: dict):
    sql = """
        INSERT INTO noun_translation(from_noun_id, to_noun_id, accuracy)
        VALUES (:from_noun_id, :to_noun_id, :accuracy)
    """

    with Database() as db:
        db.execute(sql, **noun_translation)
        noun_translation['from_noun_id'], noun_translation['to_noun_id'] = \
            noun_translation['to_noun_id'], noun_translation['from_noun_id']  # line too long so silly line break.
        db.execute(sql, **noun_translation)


def patch_noun_translation(noun_translation_id: int, data: dict):
    patchable_fields = ['from_noun_id', 'to_noun_id', 'accuracy']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `noun_translation` SET {} WHERE id=:noun_translation_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, noun_translation_id=noun_translation_id, **data)


def delete_noun_translation(first_noun_id: int, second_noun_id: int):
    sql = """
            DELETE FROM noun_translation 
            WHERE from_noun_id IN (:first_noun_id, :second_noun_id)
            AND to_noun_id IN (:first_noun_id, :second_noun_id)
          """

    with Database() as db:
        db.execute(sql, first_noun_id=first_noun_id, second_noun_id=second_noun_id)


def noun_translation_exists(noun_translation_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `noun_translation` WHERE id=:noun_translation_id);"

    with Database() as db:
        return db.scalar(sql, noun_translation_id=noun_translation_id) != 0

