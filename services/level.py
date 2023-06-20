from typing import List
from devfu.db import Database


def get_all_levels() -> List[dict]:
    sql = """
           SELECT 
               l.id, 
               l.language_id, 
               l.`code`, 
               l.title
               
           FROM `level` AS l
        """

    with Database() as db:
        return db.query_list(sql)


def get_level(level_id: int) -> dict:
    sql = """
        SELECT 
            l.id, 
            l.language_id, 
            l.`code`, 
            l.title
            
        FROM `level` AS l
        WHERE id=:level_id
        """

    with Database() as db:
        return db.query_one(sql, level_id=level_id)


def update_level(level: dict):
    sql = """
        UPDATE `level`
        SET  
            language_id=:language_id, 
            `code`=:code, 
            title=:title
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **level)


def insert_level(level: dict) -> int:
    sql = """
        INSERT INTO `level`(language_id,`code`,title)
        VALUES (:language_id,:code,:title)
    """

    with Database() as db:
        db.execute(sql, **level)
        return db.last_id()


def patch_level(level_id: int, data: dict):
    patchable_fields = ['language_id', 'code', 'title']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `level` SET {} WHERE id=:level_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, level_id=level_id, **data)


def delete_level(level_id: int):
    sql = """
        DELETE FROM level 
        WHERE id=:level_id
    """

    with Database() as db:
        db.execute(sql, level_id=level_id)


def level_exists(level_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `level` WHERE id=:level_id);"

    with Database() as db:
        return db.scalar(sql, level_id=level_id) != 0

