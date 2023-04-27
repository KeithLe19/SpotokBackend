from app.entities.ImageEntity import Image
from app.entities.TrackEntity import Track

def get_by_id(pool, id: int):
    cursor = pool.cursor()
    cursor.execute("SELECT * from track WHERE id = ?", (id, ))
    track = cursor.fetchone()
    return track

def get_all(pool):
    cursor = pool.cursor()
    cursor.execute("SELECT * from track")
    tracks = cursor.fetchall()
    return tracks

def insert(pool, new_track: Track):
    cursor = pool.cursor()
    cursor.execute("INSERT INTO track (id, track_name, href, duration_ms, origin, uri, catchy_start) VALUES (?, ?, ?, ?, ?, ?, ?)", (new_track.id, new_track.track_name, new_track.href, new_track.duration_ms, new_track.origin, new_track.uri, new_track.catchy_start))
    return cursor.lastrowid

def insert_track_artist(pool, track_id, artist_id):
    cursor = pool.cursor()
    cursor.execute("INSERT INTO track_artist (track_id, artist_id) VALUES (?, ?)", (track_id, artist_id))

def track_images(pool, track_id):
    cursor = pool.cursor()
    cursor.execute("SELECT * from track_image WHERE track_id = ?", (track_id, ))
    images = cursor.fetchall()
    return images

def insert_track_img(pool, image: Image):
    cursor = pool.cursor()
    cursor.execute("INSERT INTO track_image (href, width, height, track_id) VALUES (?, ?, ?, ?)", (image.href, image.width, image.height, image.track_id))

def insert_user_favorite_track(pool, track_id, user_id):
    cursor = pool.cursor()
    cursor.execute("INSERT INTO user_favorite_track (user_id, track_id) VALUES (?, ?)", (user_id, track_id))

def remove_user_favorite_track(pool, user_id, track_id):
    cursor = pool.cursor()
    cursor.execute("DELETE FROM user_favorite_track WHERE user_id = ? AND track_id = ?", (user_id, track_id))

def get_user_favorite_tracks(pool, user_id):
    cursor = pool.cursor()
    cursor.execute("SELECT track_id from user_favorite_track WHERE user_id = ?", (user_id, ))
    tracks = cursor.fetchall()
    return tracks
