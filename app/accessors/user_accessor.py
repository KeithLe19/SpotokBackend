from app.entities.UserEntity import User
from app import persistence
import mariadb


pool = persistence.get_db()

def get_user_by_email(email: str):
    if pool:
        cursor = pool.cursor()
        cursor.execute("SELECT pk from spotok_user WHERE email = ? LIMIT 1", (email, ))
        user_data = cursor.fetchone()
        return user_data

def insert(new_user: User):
    if pool:
        cursor = pool.cursor()
        try:
            cursor.execute("INSERT INTO spotok_user (id, email, display_name, country, phone, verified, origin) VALUES (?, ?, ?, ?, ?, ?, ?)", (new_user.id, new_user.email, new_user.display_name, new_user.country, new_user.phone, new_user.verified, new_user.origin))
            pool.commit()
            return cursor.lastrowid
        except mariadb.Error as e:
            print(f"Error: {e}")

