from typing import List
from devfu.db import Database


def get_all_recordings() -> List[dict]:
    sql = """
           SELECT 
               r.id, 
               r.noun_id, 
               r.user_id, 
               r.date_time_recorded, 
               r.filename
               
           FROM recording AS r
        """

    with Database() as db:
        return db.query_list(sql)


def get_recording(recording_id: int) -> dict:
    sql = """
        SELECT 
            r.id, 
            r.noun_id, 
            r.user_id, 
            r.date_time_recorded, 
            r.filename
            
        FROM recording AS r
        WHERE id=:recording_id
        """

    with Database() as db:
        return db.query_one(sql, recording_id=recording_id)


def update_recording(recording: dict):
    for nullable in ['user_id']:
        recording[nullable] = recording[nullable] if nullable in recording and \
                                           (recording[nullable] or not nullable.endswith('_id')) else None

    sql = """
        UPDATE recording
        SET  
            noun_id=:noun_id, 
            user_id=:user_id, 
            date_time_recorded=:date_time_recorded, 
            filename=:filename
        WHERE id=:id
    """

    with Database() as db:
        db.execute(sql, **recording)


def insert_recording(recording: dict) -> int:
    for nullable in ['user_id']:
        recording[nullable] = recording[nullable] if nullable in recording and \
                                           (recording[nullable] or not nullable.endswith('_id')) else None

    sql = """
        INSERT INTO recording(noun_id,user_id,date_time_recorded,filename)
        VALUES (:noun_id,:user_id,:date_time_recorded,:filename)
    """

    with Database() as db:
        db.execute(sql, **recording)
        return db.last_id()


def patch_recording(recording_id: int, data: dict):
    patchable_fields = ['noun_id', 'user_id', 'date_time_recorded', 'filename']

    for k in data.keys():
        if k not in patchable_fields:
            raise ValueError("Invalid field '{}'".format(k))

    used = ["`{0}`=:{0}".format(f) for f in data.keys()]

    sql = "UPDATE `recording` SET {} WHERE id=:recording_id".format(",".join(used))

    with Database() as db:
        db.execute(sql, recording_id=recording_id, **data)


def delete_recording(recording_id: int):
    sql = """
        DELETE FROM recording 
        WHERE id=:recording_id
    """

    with Database() as db:
        db.execute(sql, recording_id=recording_id)


def recording_exists(recording_id: int):
    sql = "SELECT EXISTS(SELECT 1 FROM `recording` WHERE id=:recording_id);"

    with Database() as db:
        return db.scalar(sql, recording_id=recording_id) != 0

