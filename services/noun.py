from devfu.db import Database
from typing import List

if __name__ == '__main__':
    from database import Database as new
else:
    from services.database import Database as new



def get_all_nouns() -> List[dict]:
    sql = """
           SELECT n.id, n.word, n.gender, l.title
           FROM noun as n, language as l
           WHERE n.language_id = l.id
          """
    with new() as db:
        return db.query(sql)


def get_noun_by_id(noun_id) -> List[dict]:
    sql = """
            SELECT * FROM noun WHERE id = ?
          """
    args = (noun_id,)
    with new() as db:
        return db.query(sql, args)


def update_noun(noun: dict):
    sql = """
            UPDATE noun
            SET language_id = ?,
                level_id = ?,
                gender = ?,
                word = ?
            WHERE id = ?
          """
    args = (noun['language_id'],
            noun['level_id'],
            noun['gender'],
            noun['word'],
            noun['id'])
    with new() as db:
        db.update(sql, args)


def insert_noun(noun: dict):
    sql = """
            INSERT INTO 
                noun(language_id, level_id, gender, word)
            VALUES
                (?, NULL, ?, ?)
          """
    args = (noun['language_id'],
            noun['gender'],
            noun['word'])
    with new() as db:
        db.insert(sql, args)

# def insert_noun(noun: dict) -> int:
#     for nullable in ['level_id', 'gender']:
#         noun[nullable] = noun[nullable] if nullable in noun and \
#                                            (noun[nullable] or not nullable.endswith('_id')) else None
#
#     sql = """
#         INSERT INTO noun(language_id,level_id,gender,word)
#         VALUES (:language_id,:level_id,:gender,:word)
#     """
#
#     with Database() as db:
#         db.execute(sql, **noun)
#         return db.last_id()


def patch_noun(noun_id: int, data: dict):
    patchable_fields = ['language_id', 'level_id', 'gender', 'word']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `noun` SET {} WHERE id=:noun_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, noun_id=noun_id, **data)


def delete_noun(noun_id: int):
    sql = """
        DELETE FROM noun 
        WHERE id=:noun_id
    """

    with Database() as db:
        db.execute(sql, noun_id=noun_id)


def noun_exists(noun_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `noun` WHERE id=:noun_id);"

    with Database() as db:
        return db.scalar(sql, noun_id=noun_id) != 0


def stress_test():
    sql = '''
            UPDATE noun
            SET language_id = ?,
                level_id = ?,
                gender = ?,
                word = ?
            WHERE id = ?
          '''
    with new() as db:
        for item in db.query(sql):
            print(item)


if __name__ == '__main__':
    stress_test()
