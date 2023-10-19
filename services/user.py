from typing import List
from devfu.db import Database


def get_all_users() -> List[dict]:
    sql = """
           SELECT 
               u.id, 
               u.email, 
               u.`password`, 
               u.role
               
           FROM `user` AS u
        """

    with Database() as db:
        return db.query_list(sql)


def get_user() -> dict:
    sql = """
        SELECT 
            u.id, 
            u.email, 
            u.`password`, 
            u.role
            
        FROM `user` AS u
        WHERE 
        """

    with Database() as db:
        return db.query_one(sql, )


def find_user(email: str) -> dict:
    sql = """
        SELECT 
            u.id, 
            u.email, 
            u.`password`, 
            u.role,
            u.timezone
        FROM `user` AS u
        WHERE LOWER(email) = LOWER(:email)
    """

    with Database() as db:
        return db.query_one(sql, email=email)  # Noqa

def update_user(user: dict):
    pass


def insert_user(user: dict):
    sql = """
            INSERT INTO user(email, password, `role`, timezone)
            VALUES (:email, :password, :role, :timezone)
        """

    with Database() as db:
        db.execute(sql, **user)


def patch_user(user_id: int, data: dict):
    pass


def delete_user():
    pass


def user_exists(data) -> bool:
    pass
