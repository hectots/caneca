import json

from .common import connect


def is_new_user(sub):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM security_user WHERE sub = %s", (sub,))
            result = cur.fetchone()

            return result is None


def add_pending_user(user):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO security_pending_user (sub, payload) VALUES (%s, %s) ON CONFLICT (sub) DO NOTHING", (user['sub'], json.dumps(user)))
        conn.commit()


def accept_pending_user(user):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO security_user (sub, name)
                        SELECT sub, payload->>'name' AS name 
                        FROM security_pending_user WHERE sub = %s
                        """, (user, ))
        conn.commit()


def is_accepted_user(sub):
    return not is_new_user(sub)
