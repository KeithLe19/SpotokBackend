from app.entities.GenreEntity import Genre
from app import persistence
import mariadb



def get_by_id(pool, id: int):
    cursor = pool.cursor()
    cursor.execute("SELECT * from genre WHERE pk = ? LIMIT 1", (id, ))
    genre_object = cursor.fetchone()
    genre = Genre(genre_object["name"], genre_object["pk"])
    return genre

def get_all(pool):
    cursor = pool.cursor()
    cursor.execute("SELECT * from genre limit 30")
    genres = cursor.fetchall()
    return genres

def get_user_genres(pool, user_id):
    cursor = pool.cursor()
    cursor.execute("SELECT g.pk, g.genre_name FROM genre g JOIN user_selected_genre ug ON g.pk = ug.genre_id WHERE ug.user_id = ?", (user_id, ))
    genres = cursor.fetchall()
    return genres

def delete_user_genres(pool, user_id):
    cursor = pool.cursor()
    try:
        cursor.execute("DELETE FROM user_selected_genre WHERE user_id = ?", (user_id, ))
    except mariadb.Error as e:
        print(f"Error: {e}")

def insert_user_genre(pool, user_id, genre_id):
    cursor = pool.cursor()
    try:
        cursor.execute("INSERT INTO user_selected_genre (user_id, genre_id) VALUES (?, ?)", (user_id, genre_id, ))
        return cursor.lastrowid
    except mariadb.Error as e:
        print(f"Error: {e}")

def insert(pool, new_genre: Genre):
    cursor = pool.cursor()
    try:
        cursor.execute("INSERT INTO genre (name) VALUES (?)", (new_genre.name))
        pool.commit()
        return cursor.lastrowid
    except mariadb.Error as e:
        print(f"Error: {e}")
