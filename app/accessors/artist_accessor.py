import mariadb
from app.entities.ArtistEntity import Artist

def get_by_id(pool, id):
    cursor = pool.cursor()
    cursor.execute("SELECT * from artist WHERE id = ?", (id,))
    artist = cursor.fetchone()
    return artist 

def get_arist_ids_by_track_id(pool, track_id):
    cursor = pool.cursor()
    cursor.execute("SELECT artist_id from track_artist WHERE track_id = ?", (track_id,))
    artist = cursor.fetchall()
    return artist 

def get_all(pool):
    cursor = pool.cursor()
    cursor.execute("SELECT * from artist")
    artists = cursor.fetchall()
    return artists

def insert(pool, new_artist: Artist):
    cursor = pool.cursor()
    try:
        cursor.execute("INSERT INTO artist (id, artist_name, href, origin, uri) VALUES (?, ?, ?, ?, ?)", (new_artist.id, new_artist.artist_name, new_artist.href, new_artist.origin, new_artist.uri))
        return cursor.lastrowid
    except mariadb.Error as e:
        print(f"Error: {e}")
