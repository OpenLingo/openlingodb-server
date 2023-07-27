from typing import List
from services.database import Database

# Start using DEVFU.db to import Database for context managers.


def get_all_nouns() -> List[dict]:
    sql = """
           SELECT n.id, n.word, n.gender, l.title
           FROM noun as n, language as l
           WHERE n.language_id = l.id
           ORDER BY n.id
          """
    with Database() as db:
        return db.query(sql)


def get_noun_by_id(noun_id) -> dict:
    sql = """
            SELECT * 
            FROM noun 
            WHERE id = ?
          """
    args = (noun_id,)

    with Database() as db:
        return db.query(sql, args)[0]


def verify_noun_by_word(noun) -> bool:
    sql = """
            SELECT EXISTS(
                SELECT 1 FROM noun WHERE word = ?
            ) AS `exists`
          """
    args = (noun['word'],)

    with Database() as db:
        return bool(db.query(sql, args)[0]['exists'])


def insert_noun(noun: dict):
    sql = """
            INSERT INTO noun(language_id, level_id, gender, word)
            VALUES (?, NULL, ?, ?)
          """
    args = (noun['language_id'],
            None if noun['gender'] == 'NULL' else noun['gender'],
            noun['word'])

    if not verify_noun_by_word(noun):
        with Database() as db:
            db.insert(sql, args)
    else:
        print("that noun is already in the database")


def update_noun(noun: dict):
    sql = """
            UPDATE noun
            SET language_id = ?, level_id = ?, gender = ?, word = ?
            WHERE id = ?
          """
    args = (noun['language_id'], noun['level_id'], noun['gender'], noun['word'], noun['id'])

    with Database() as db:
        db.update(sql, args)


# def patch_noun(noun_id: int, data: dict):
#     patchable_fields = ['language_id', 'level_id', 'gender', 'word']
#
#     for k in data.keys():
#         if k not in patchable_fields:
#             raise ValueError("Invalid field '{}'".format(k))
#
#     used = ["`{0}`=:{0}".format(f) for f in data.keys()]
#
#     sql = "UPDATE `noun` SET {} WHERE id=:noun_id".format(",".join(used))
#
#     with Database() as db:
#         db.execute(sql, noun_id=noun_id, **data)


# def delete_noun(noun_id: int):
#     sql = """
#         DELETE FROM noun
#         WHERE id=:noun_id
#     """
#
#     with Database() as db:
#         db.execute(sql, noun_id=noun_id)
