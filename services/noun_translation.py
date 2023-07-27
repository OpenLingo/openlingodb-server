from typing import List
from services.database import Database


def get_translations(noun_id) -> List[dict]:
    sql = """
            SELECT n.id, n.word
            FROM noun AS n, noun_translation AS nt
            WHERE nt.from_noun_id = ?
            AND n.id = nt.to_noun_id
          """
    args = (noun_id,)

    with Database() as db:
        return db.query(sql, args)


def add_translation(data: dict):
    sql = """
            INSERT INTO noun_translation(from_noun_id, to_noun_id, accuracy)
            VALUES (?, ?, ?)
          """
    args = (data['from_noun_id'], data['to_noun_id', data['accuracy']])

    with Database() as db:
        db.insert(sql, args)
