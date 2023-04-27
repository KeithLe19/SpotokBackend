from app.entities.AuthEntity import Auth
from app import persistence
import mariadb


pool = persistence.get_db()


def insert(new_auth: Auth):
    if pool: 
        cur = pool.cursor()
        try:
            cur.execute("INSERT INTO auth (email, access_token, refresh_token, auth_type, expires_at) VALUES (?, ?, ?, ?, ?, ?)", (new_auth.email, new_auth.access_token, new_auth.refresh_token, new_auth.auth_type, new_auth.expires_at))
            pool.commit()
            return cur.lastrowid
        except mariadb.Error as e:
            print(f"Error: {e}")

