from typing import List
from devfu.db import Database


def get_all_feedbacks() -> List[dict]:
    sql = """
           SELECT 
               f.id, 
               f.user_id, 
               f.`comment`, 
               f.json_data, 
               f.entity, 
               f.entity_id, 
               f.is_approved
               
           FROM feedback AS f
        """

    with Database() as db:
        return db.query_list(sql)


def get_feedback(feedback_id: int) -> dict:
    sql = """
        SELECT 
            f.id, 
            f.user_id, 
            f.`comment`, 
            f.json_data, 
            f.entity, 
            f.entity_id, 
            f.is_approved
            
        FROM feedback AS f
        WHERE id=:feedback_id
        """

    with Database() as db:
        return db.query_one(sql, feedback_id=feedback_id)


def update_feedback(feedback: dict):
    for nullable in ['user_id', 'json_data', 'entity', 'entity_id', 'is_approved']:
        feedback[nullable] = feedback[nullable] if nullable in feedback and \
                                           (feedback[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE feedback
        SET  
            user_id=:user_id, 
            `comment`=:comment, 
            json_data=:json_data, 
            entity=:entity, 
            entity_id=:entity_id, 
            is_approved=:is_approved
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **feedback)


def insert_feedback(feedback: dict) -> int:
    for nullable in ['user_id', 'json_data', 'entity', 'entity_id', 'is_approved']:
        feedback[nullable] = feedback[nullable] if nullable in feedback and \
                                           (feedback[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO feedback(user_id,`comment`,json_data,entity,entity_id,is_approved)
        VALUES (:user_id,:comment,:json_data,:entity,:entity_id,:is_approved)
    """

    with Database() as db:
        db.execute(sql, **feedback)
        return db.last_id()


def patch_feedback(feedback_id: int, data: dict):
    patchable_fields = ['user_id', 'comment', 'json_data', 'entity', 'entity_id', 'is_approved']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `feedback` SET {} WHERE id=:feedback_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, feedback_id=feedback_id, **data)


def delete_feedback(feedback_id: int):
    sql = """
        DELETE FROM feedback 
        WHERE id=:feedback_id
    """

    with Database() as db:
        db.execute(sql, feedback_id=feedback_id)


def feedback_exists(feedback_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `feedback` WHERE id=:feedback_id);"

    with Database() as db:
        return db.scalar(sql, feedback_id=feedback_id) != 0

