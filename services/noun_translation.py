from typing import List
from services.database import Database


def get_translations(noun_id) -> List[dict]:
    sql = """
            SELECT id, word
            FROM noun
            WHERE id != ?
            AND id IN (
                SELECT from_noun_id 
                FROM noun_translation 
                WHERE to_noun_id = ?
            
                UNION
                
                SELECT to_noun_id 
                FROM noun_translation
                WHERE from_noun_id = ?
            );
          """
    args = (noun_id, noun_id, noun_id)

    with Database() as db:
        return db.query(sql, args)


def insert_translation(data: dict):
    # Inserts twice. Once as the data is provided, and second time with the from_noun_id
    # an to_noun_id entries swapped in order to create a translation entry for the
    # relationship in both directions.
    sql = """
            INSERT INTO noun_translation(from_noun_id, to_noun_id, accuracy)
            VALUES (?, ?, ?)
          """
    args = (data['from_noun_id'], data['to_noun_id'], data['accuracy'])

    with Database() as db:
        db.insert(sql, args)
        args = (args[1], args[0], args[2])  # Swap from_noun_id and to_noun_id
        db.insert(sql, args)


def delete_translation(data: List):
    sql = """
            DELETE FROM noun_translation
            WHERE from_noun_id IN (?, ?)
            AND to_noun_id IN (?, ?)
          """
    args = (data[0], data[1], data[0], data[1])

    with Database() as db:
        db.delete(sql, args)
