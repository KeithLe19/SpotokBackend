import spotipy
import json
from app import persistence
from app.accessors import track_accessor
from app.accessors import genre_accessor
from app.accessors import artist_accessor
from app.managers.MessageManager import MessageManager
from app.managers.OpenAIManager import OpenAIManager



class SpotifyManager:
    def __init__(self) -> None:
        self.messageManager = MessageManager()
        self.openAIManager = OpenAIManager()
        
    # Add the given tracks to the users spotify playlist
    def addToPlaylist(self, token, tracks, playlist):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=token)

            # Not using because we avoid making too many api calls
            #user id
            user = sp.me()
            user_id = user["id"]

            playlistID = playlist["id"]
            
            if playlistID is None:
                print("Creating a new playlist for user.......") 
                # Call to create new playlist
                newPlaylist = sp.user_playlist_create(user=user_id, 
                                        name=playlist["name"], 
                                        public=True, 
                                        collaborative=False, 
                                        description="")

                # Get updated users playlists
                playlistID = newPlaylist["id"]
                        
            # Add the track list into the playlist
            sp.playlist_add_items(playlistID, tracks)
            return self.messageManager.getMessage(isError=False, 
                                                  message="Successfully added", 
                                                  statusCode=200, 
                                                  data=None)
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 
              
    def getPlaylists(self, token):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=token)

            # Get user playlists
            playlistsObj = sp.current_user_playlists(20)
            return self.messageManager.getMessage(isError=False, 
                                                  message="Successfully retrieved playlists", 
                                                  statusCode=200, 
                                                  data=playlistsObj)
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None)
        
    def getArtist(self, token, genres, artistList):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=token)

            artists = ""
            strGenres = ""
            artistName = '<insert_artist_name_here>'
            maxct = len(genres) - 1
            for ct, val in enumerate(genres):
                artistName = artistList[genres[ct]]
                strGenres += val
                
                # Get artists ID
                searchResult = sp.search(q=artistName, limit=1, offset=0, type='artist', market='US')
                artists += searchResult['artists']['items'][0]['id']
                if (ct < maxct): 
                    artists += ","
                    strGenres += ","
            return {'artist': artists, 'strGenres' : strGenres}
        except:
            return None
        
    def getTrackID(self, token, song):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=token)
            
            # Get track ID
            searchResult = sp.search(q=song, limit=1, offset=0, type='track', market='US')
            return searchResult['tracks']['items'][0]['id']
        except spotipy.exceptions.SpotifyException as err:
            return None

    def getRecommendations(self, token, artists, genres, tracks):
        try:
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=token)
            
            # Make lists
            artistsList = artists.split(",")
            genresList = genres.split(",")
            
            # Make a list of track ID
            tracksList = []
            for track in tracks.split(","):
                tid = self.getTrackID(token=token, song=track)
                if tid is None:
                    return None
                tracksList.append(tid)

            # Get recommendations
            recommendations = sp.recommendations(seed_artists=artistsList, 
                                                 seed_genres=genresList, 
                                                 seed_tracks=tracksList, 
                                                 limit=10, 
                                                 country='US')
   
            return recommendations
        except spotipy.exceptions.SpotifyException as err:
            return None
        
    def getInitialRecommendation(self, token, genres):

        # Use auth token to access spotify
        artistList = self.openAIManager.getInitialRecommendation(genres=genres)
        if artistList is None:
            return self.messageManager.getMessage(isError=True, message="ChatGPT Error", statusCode=400, data=None)
            
        artistsGenres = self.getArtist(token=token, genres=genres, artistList=artistList)
        if artistsGenres is None:
            return self.messageManager.getMessage(isError=True, message="Spotify Search Artist Error", statusCode=400, data=None)
        
        # Get recommendations
        recommendations = self.getRecommendations(token=token, 
                                                  artists=artistsGenres['artist'], 
                                                  genres=artistsGenres['strGenres'], 
                                                  tracks=artistList['song'])
        
        # Set time stamps on each song
        ts = self.openAIManager.getTimeStamps(spotifyRecommendations=recommendations)
        return self.messageManager.getMessage(isError=False, message="Success", statusCode=200, data=ts)

    def start_track(self, token, device_id, track_uri, position_ms):
        try:
            uris = []
            uris.append(track_uri)
            # Use auth token to access spotify
            sp = spotipy.Spotify(auth=token)

            sp.start_playback(device_id, uris=uris, position_ms=position_ms )
            return self.messageManager.getMessage(isError=False, 
                                                  message="Track started", 
                                                  statusCode=204, 
                                                  data=None)
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 

    def pause_track(self, token, device_id):
        try:
            sp = spotipy.Spotify(auth=token)

            sp.pause_playback(device_id)

            return self.messageManager.getMessage(isError=False, 
                                                  message="Track paused", 
                                                  statusCode=204, 
                                                  data=None)
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None)

    def get_recommendations_v2(self, access_token):
        try:
            sp = spotipy.Spotify(auth=access_token)

            # get current user
            current_user = sp.me()
            user_id = current_user["id"]
            pool = persistence.get_db()
            if pool:
                user_genres = genre_accessor.get_user_genres(pool, user_id)
                if user_genres:
                    genres_names = [t[1] for t in user_genres]
                    user_liked_tracks = track_accessor.get_user_favorite_tracks(pool, user_id)
                    if not user_liked_tracks:
                        user_top_tracks = sp.current_user_top_tracks(limit=1)
                        top_track = user_top_tracks["items"][0]
                        track_id = top_track["id"]
                        track_artist_id = top_track["artists"][0]["id"]
                    else:
                        track_ids = [t[0] for t in user_liked_tracks]
                        track_id = track_ids[len(track_ids) - 1]
                        track_artist_ids = artist_accessor.get_arist_ids_by_track_id(pool, track_id) 
                        track_artist_id = track_artist_ids[0][0]
                    

                    tracks = []
                    tracks.append(track_id)
                    artists = []
                    artists.append(track_artist_id)
                    recommendation = sp.recommendations(artists, genres_names, tracks, limit=10)

                    return self.messageManager.getMessage(isError=False, 
                                                          message="Success", 
                                                          statusCode=200, 
                                                          data=recommendation["tracks"])

            return self.messageManager.getMessage(isError=True, message="Internal Error", statusCode=500, data=None) 
        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None)
