from typing import List
from devfu.db import Database


def get_all_topics() -> List[dict]:
    sql = """
           SELECT 
               t.id, 
               t.level_id, 
               t.title
               
           FROM topic AS t
        """

    with Database() as db:
        return db.query_list(sql)


def get_topic(topic_id: int) -> dict:
    sql = """
        SELECT 
            t.id, 
            t.level_id, 
            t.title
            
        FROM topic AS t
        WHERE id=:topic_id
        """

    with Database() as db:
        return db.query_one(sql, topic_id=topic_id)


def update_topic(topic: dict):
    for nullable in ['level_id']:
        topic[nullable] = topic[nullable] if nullable in topic and \
                                           (topic[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE topic
        SET  
            level_id=:level_id, 
            title=:title
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **topic)


def insert_topic(topic: dict) -> int:
    for nullable in ['level_id']:
        topic[nullable] = topic[nullable] if nullable in topic and \
                                           (topic[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO topic(level_id,title)
        VALUES (:level_id,:title)
    """

    with Database() as db:
        db.execute(sql, **topic)
        return db.last_id()


def patch_topic(topic_id: int, data: dict):
    patchable_fields = ['level_id', 'title']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `topic` SET {} WHERE id=:topic_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, topic_id=topic_id, **data)


def delete_topic(topic_id: int):
    sql = """
        DELETE FROM topic 
        WHERE id=:topic_id
    """

    with Database() as db:
        db.execute(sql, topic_id=topic_id)


def topic_exists(topic_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `topic` WHERE id=:topic_id);"

    with Database() as db:
        return db.scalar(sql, topic_id=topic_id) != 0

