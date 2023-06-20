from typing import List
from devfu.db import Database


def get_all_app_logs() -> List[dict]:
    sql = """
           SELECT 
               al.id, 
               al.user_id, 
               al.log_level, 
               al.message, 
               al.date_time, 
               al.creator, 
               al.`source`, 
               al.request
               
           FROM app_log AS al
        """

    with Database() as db:
        return db.query_list(sql)


def get_app_log(app_log_id: int) -> dict:
    sql = """
        SELECT 
            al.id, 
            al.user_id, 
            al.log_level, 
            al.message, 
            al.date_time, 
            al.creator, 
            al.`source`, 
            al.request
            
        FROM app_log AS al
        WHERE id=:app_log_id
        """

    with Database() as db:
        return db.query_one(sql, app_log_id=app_log_id)


def update_app_log(app_log: dict):
    for nullable in ['user_id']:
        app_log[nullable] = app_log[nullable] if nullable in app_log and \
                                           (app_log[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE app_log
        SET  
            user_id=:user_id, 
            log_level=:log_level, 
            message=:message, 
            date_time=:date_time, 
            creator=:creator, 
            `source`=:source, 
            request=:request
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **app_log)


def insert_app_log(app_log: dict) -> int:
    for nullable in ['user_id']:
        app_log[nullable] = app_log[nullable] if nullable in app_log and \
                                           (app_log[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO app_log(user_id,log_level,message,date_time,creator,`source`,request)
        VALUES (:user_id,:log_level,:message,:date_time,:creator,:source,:request)
    """

    with Database() as db:
        db.execute(sql, **app_log)
        return db.last_id()


def patch_app_log(app_log_id: int, data: dict):
    patchable_fields = ['user_id', 'log_level', 'message', 'date_time', 'creator', 'source', 'request']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `app_log` SET {} WHERE id=:app_log_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, app_log_id=app_log_id, **data)


def delete_app_log(app_log_id: int):
    sql = """
        DELETE FROM app_log 
        WHERE id=:app_log_id
    """

    with Database() as db:
        db.execute(sql, app_log_id=app_log_id)


def app_log_exists(app_log_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `app_log` WHERE id=:app_log_id);"

    with Database() as db:
        return db.scalar(sql, app_log_id=app_log_id) != 0

