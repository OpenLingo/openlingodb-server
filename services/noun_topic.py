from typing import List
from devfu.db import Database


def get_all_noun_topics() -> List[dict]:
    sql = """
           SELECT 
               nt.id, 
               nt.noun_id, 
               nt.topic_id
               
           FROM noun_topic AS nt
        """

    with Database() as db:
        return db.query_list(sql)


def get_noun_topic(noun_topic_id: int) -> dict:
    sql = """
        SELECT 
            nt.id, 
            nt.noun_id, 
            nt.topic_id
            
        FROM noun_topic AS nt
        WHERE id=:noun_topic_id
        """

    with Database() as db:
        return db.query_one(sql, noun_topic_id=noun_topic_id)


def update_noun_topic(noun_topic: dict):
    sql = """
        UPDATE noun_topic
        SET  
            noun_id=:noun_id, 
            topic_id=:topic_id
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **noun_topic)


def insert_noun_topic(noun_topic: dict) -> int:
    sql = """
        INSERT INTO noun_topic(noun_id,topic_id)
        VALUES (:noun_id,:topic_id)
    """

    with Database() as db:
        db.execute(sql, **noun_topic)
        return db.last_id()


def patch_noun_topic(noun_topic_id: int, data: dict):
    patchable_fields = ['noun_id', 'topic_id']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `noun_topic` SET {} WHERE id=:noun_topic_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, noun_topic_id=noun_topic_id, **data)


def delete_noun_topic(noun_topic_id: int):
    sql = """
        DELETE FROM noun_topic 
        WHERE id=:noun_topic_id
    """

    with Database() as db:
        db.execute(sql, noun_topic_id=noun_topic_id)


def noun_topic_exists(noun_topic_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `noun_topic` WHERE id=:noun_topic_id);"

    with Database() as db:
        return db.scalar(sql, noun_topic_id=noun_topic_id) != 0

