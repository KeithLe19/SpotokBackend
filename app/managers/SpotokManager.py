import spotipy
import mariadb
from app.accessors import track_accessor
from app.accessors import artist_accessor
from app.accessors import genre_accessor
from app.entities.ArtistEntity import Artist
from app.entities.TrackEntity import Track
from app.entities.ImageEntity import Image
from app.managers.MessageManager import MessageManager
from app import persistence



class SpotokManager:
    def __init__(self):
        self.messageManager = MessageManager()

    def get_track_by_id(self, id):
        pool = persistence.get_db()
        track = track_accessor.get_by_id(pool, id)
        return track

    def get_all_genres(self):
        pool = persistence.get_db()
        if pool:
            genres = genre_accessor.get_all(pool)
            genres_list = []
            for genre_pair in genres:
                g_dict = dict()
                g_dict["id"] = genre_pair[0]
                g_dict["name"] = genre_pair[1]
                genres_list.append(g_dict)
            return self.messageManager.getMessage(isError=False, 
                                                    message="Retrieved all genres", 
                                                    statusCode=200, 
                                                    data=genres_list)
        return self.messageManager.getMessage(isError=True, message="Internal Error", statusCode=500, data=None) 

    def insert_user_genre(self, access_token, genre_ids):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=access_token)

            # get current user
            current_user = sp.me()
            user_id = current_user["id"]

            pool = persistence.get_db()
            if pool:
                genre_accessor.delete_user_genres(pool, user_id)
                for genre_id in genre_ids:
                    genre_accessor.insert_user_genre(pool, user_id, genre_id)
                pool.commit()
                return self.messageManager.getMessage(isError=False, 
                                                      message="genres inserted", 
                                                      statusCode=204, 
                                                      data=None)
            return self.messageManager.getMessage(isError=True, message="Internal Error", statusCode=500, data=None) 
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 
        except mariadb.Error:
            return self.messageManager.getMessage(isError=True, message="Database error", statusCode=500, data=None) 

    def get_user_genres(self, access_token):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=access_token)

            # get current user
            current_user = sp.me()
            user_id = current_user["id"]

            pool = persistence.get_db()
            if pool:
                genres = genre_accessor.get_user_genres(pool, user_id)
                genres_list = []
                for genre_pair in genres:
                    g_dict = dict()
                    g_dict["id"] = genre_pair[0]
                    g_dict["name"] = genre_pair[1]
                    genres_list.append(g_dict)
                return self.messageManager.getMessage(isError=False, 
                                                      message="Retrieved all user genres", 
                                                      statusCode=200, 
                                                      data=genres_list)
            return self.messageManager.getMessage(isError=True, message="Internal Error", statusCode=500, data=None) 
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 
        except mariadb.Error:
            return self.messageManager.getMessage(isError=True, message="Database error", statusCode=500, data=None) 


    def add_track_to_user_library(self, access_token, track_id):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=access_token)

            # get current user
            current_user = sp.me()
            user_id = current_user["id"]


            pool = persistence.get_db()
            if pool:
                track = track_accessor.get_by_id(pool, track_id)
                if track is None:
                    # get current track
                    spt_track = sp.track(track_id)

                    # insert track 
                    new_track = Track(spt_track["id"], spt_track["name"], spt_track["external_urls"]["spotify"], spt_track["duration_ms"], origin = "spotify", uri=spt_track["uri"])
                    track_accessor.insert(pool, new_track)
                    

                    # insert artist
                    track_artists = spt_track["artists"]
                    for art in track_artists:
                        artist_obj = Artist(art["id"], art["name"], art["href"], "spotify", art["uri"] )
                        artist_accessor.insert(pool, artist_obj)
                        # insert to track_artist table
                        track_accessor.insert_track_artist(pool, track_id, art["id"])

                    # insert images
                    track_album = spt_track["album"]
                    track_images = track_album["images"]
                    for img in track_images:
                        img_obj = Image(img["url"], img["width"], img["height"], track_id)
                        track_accessor.insert_track_img(pool, img_obj)


                # insert to user_favorite_track table
                track_accessor.insert_user_favorite_track(pool, user_id=user_id, track_id=track_id)
                pool.commit()

                # get metadata
                track_meta_data = self.get_track_meta_data(track_id)
                return self.messageManager.getMessage(isError=False, 
                                                      message="Successfully added", 
                                                      statusCode=200, 
                                                      data=track_meta_data)
            return self.messageManager.getMessage(isError=True, message="Internal Error", statusCode=500, data=None) 
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 
        except mariadb.Error as e:
            print(e)
            return self.messageManager.getMessage(isError=True, message="Some error occurred", statusCode=500, data=None) 

    def remove_track_from_user_library(self, access_token, track_id):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=access_token)

            # get current user
            current_user = sp.me()
            user_id = current_user["id"]

            pool = persistence.get_db()
            if pool:
                track_accessor.remove_user_favorite_track(pool, user_id, track_id)
                pool.commit()
                return self.messageManager.getMessage(isError=False, 
                                                      message="Successfully removed", 
                                                      statusCode=204, 
                                                      data=None)
            return self.messageManager.getMessage(isError=True, message="Internal Error", statusCode=500, data=None) 
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 
        except mariadb.Error:
            return self.messageManager.getMessage(isError=True, message="Database error", statusCode=500, data=None) 

    def get_user_library(self, access_token):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=access_token)

            # get current user
            current_user = sp.me()
            user_id = current_user["id"]


            pool = persistence.get_db()
            if pool:
                track_ids = track_accessor.get_user_favorite_tracks(pool, user_id)
                track_list = []
                print(track_ids)
                for id_tuple in track_ids:
                    id = id_tuple[0]
                    track_meta_data = self.get_track_meta_data(id)
                    track_list.append(track_meta_data)
                return self.messageManager.getMessage(isError=False, 
                                                      message="Successfully added", 
                                                      statusCode=200, 
                                                      data=track_list)
            return self.messageManager.getMessage(isError=True, message="Internal Error", statusCode=500, data=None) 
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 
        except mariadb.Error as e:
            return self.messageManager.getMessage(isError=True, message="Database error", statusCode=500, data=None) 

    def get_track_meta_data(self, track_id):
        pool = persistence.get_db()
        # get track object
        track = track_accessor.get_by_id(pool, track_id) 

        # get artists
        artist_list = []
        artist_ids = artist_accessor.get_arist_ids_by_track_id(pool, track_id)
        print(artist_ids)
        for id_tuple in artist_ids:
            id = id_tuple[0]
            artist = artist_accessor.get_by_id(pool, id)
            artist_obj = dict()
            artist_obj["href"] = artist[4]
            artist_obj["id"] = artist[1]
            artist_obj["name"] = artist[2]
            artist_obj["uri"] = artist[3]
            artist_obj["images"] = []
            artist_list.append(artist_obj)
        
        #get image
        image_list = []
        images = track_accessor.track_images(pool, track_id)
        for img in images:
            img_obj = dict()
            img_obj["url"] = img[1]
            img_obj["width"] = img[2]
            img_obj["height"] = img[3]
            image_list.append(img_obj)

        track_obj = dict()
        print(track)

        track_obj["id"] = track[0]
        track_obj["external_id"] = track[1]
        track_obj["name"] = track[2]
        track_obj["href"] = track[4]
        track_obj["duration_ms"] = track[5]
        track_obj["origin"] = track[7]
        track_obj["artists"] = artist_list
        track_obj["images"] = image_list

        return track_obj
