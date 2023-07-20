from typing import List
from services.database import Database


def get_all_languages() -> List[dict]:
    sql = """
               SELECT *
               FROM language
              """

    with Database() as db:
        return db.query(sql)


def get_language(language_id: int) -> dict:
    sql = """
        SELECT *  
        FROM `language`
        WHERE id = ?
        """
    args = (language_id,)

    with Database() as db:
        return db.query(sql, args)[0]


# def update_language(language: dict):
#     for nullable in ['is_gendered']:
#         language[nullable] = language[nullable] if nullable in language and \
#                                            (language[nullable] or not nullable.endswith('_id')) else None
#
#     sql = """
#         UPDATE `language`
#         SET
#             `code`=:code,
#             title=:title,
#             is_gendered=:is_gendered
#         WHERE id=:id
#     """
#
#     with Database() as db:
#         db.execute(sql, **language)


# def insert_language(language: dict) -> int:
#     for nullable in ['is_gendered']:
#         language[nullable] = language[nullable] if nullable in language and \
#                                            (language[nullable] or not nullable.endswith('_id')) else None
#
#     sql = """
#         INSERT INTO `language`(`code`,title,is_gendered)
#         VALUES (:code,:title,:is_gendered)
#     """
#
#     with Database() as db:
#         db.execute(sql, **language)
#         return db.last_id()


# def patch_language(language_id: int, data: dict):
#     patchable_fields = ['code', 'title', 'is_gendered']
#
#     for k in data.keys():
#         if k not in patchable_fields:
#             raise ValueError("Invalid field '{}'".format(k))
#
#     used = ["`{0}`=:{0}".format(f) for f in data.keys()]
#
#     sql = "UPDATE `language` SET {} WHERE id=:language_id".format(",".join(used))
#
#     with Database() as db:
#         db.execute(sql, language_id=language_id, **data)


# def delete_language(language_id: int):
#     sql = """
#         DELETE FROM language
#         WHERE id=:language_id
#     """
#
#     with Database() as db:
#         db.execute(sql, language_id=language_id)


# def language_exists(language_id: int):
#     sql = "SELECT EXISTS(SELECT 1 FROM `language` WHERE id=:language_id);"
#
#     with Database() as db:
#         return db.scalar(sql, language_id=language_id) != 0

