from typing import List
from devfu.db import Database


def get_all_topic_childs() -> List[dict]:
    sql = """
           SELECT 
               tc.id, 
               tc.child_topic_id, 
               tc.parent_topic_id
               
           FROM topic_child AS tc
        """

    with Database() as db:
        return db.query_list(sql)


def get_topic_child(topic_child_id: int) -> dict:
    sql = """
        SELECT 
            tc.id, 
            tc.child_topic_id, 
            tc.parent_topic_id
            
        FROM topic_child AS tc
        WHERE id=:topic_child_id
        """

    with Database() as db:
        return db.query_one(sql, topic_child_id=topic_child_id)


def update_topic_child(topic_child: dict):
    sql = """
        UPDATE topic_child
        SET  
            child_topic_id=:child_topic_id, 
            parent_topic_id=:parent_topic_id
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **topic_child)


def insert_topic_child(topic_child: dict) -> int:
    sql = """
        INSERT INTO topic_child(child_topic_id,parent_topic_id)
        VALUES (:child_topic_id,:parent_topic_id)
    """

    with Database() as db:
        db.execute(sql, **topic_child)
        return db.last_id()


def patch_topic_child(topic_child_id: int, data: dict):
    patchable_fields = ['child_topic_id', 'parent_topic_id']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `topic_child` SET {} WHERE id=:topic_child_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, topic_child_id=topic_child_id, **data)


def delete_topic_child(topic_child_id: int):
    sql = """
        DELETE FROM topic_child 
        WHERE id=:topic_child_id
    """

    with Database() as db:
        db.execute(sql, topic_child_id=topic_child_id)


def topic_child_exists(topic_child_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `topic_child` WHERE id=:topic_child_id);"

    with Database() as db:
        return db.scalar(sql, topic_child_id=topic_child_id) != 0

