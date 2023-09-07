from typing import List
from devfu.db import Database


def get_all_nouns() -> List[dict]:
    sql = """
           SELECT n.id, n.word, n.gender, n.language_id
           FROM noun as n, language as l
           WHERE n.language_id = l.id
           ORDER BY n.id
          """
    with Database() as db:
        return db.query_list(sql)


def get_nouns_by_string(search_term) -> List[dict]:
    sql = """
            SELECT *
            FROM noun
            WHERE word LIKE(:search_term)
          """

    with Database() as db:
        return db.query_list(sql, search_term=search_term + '%')


def get_noun_by_id(noun_id: int) -> dict:
    sql = """
            SELECT
                n.id,
                n.language_id,
                n.level_id,
                n.gender,
                n.word

            FROM noun AS n
            WHERE id=:noun_id
            """

    with Database() as db:
        return db.query_one(sql, noun_id=noun_id)


def verify_noun_by_word(noun) -> bool:
    sql = """
            SELECT EXISTS(
                SELECT 1 FROM noun WHERE word = :noun
            ) AS `exists`
          """

    with Database() as db:
        return bool(db.scalar(sql, noun=noun))


def insert_noun(noun: dict):
    # Ask andrew about this.
    for nullable in ['level_id', 'gender']:
        #     if noun[nullable] == 0 or 'NULL':
        #         noun[nullable] = None
        noun[nullable] = noun[nullable] if nullable in noun and \
                                       (noun[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO noun(language_id,level_id,gender,word)
        VALUES (:language_id,:level_id,:gender,:word)
    """

    if verify_noun_by_word(noun['word']):
        return
    with Database() as db:
        db.execute(sql, **noun)


def update_noun(noun: dict):
    for nullable in ['level_id', 'gender']:
        noun[nullable] = noun[nullable] if nullable in noun and \
                                           (noun[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE noun
        SET
            language_id=:language_id,
            level_id=:level_id,
            gender=:gender,
            word=:word
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **noun)

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
