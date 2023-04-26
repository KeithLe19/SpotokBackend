import spotipy

from app.entities.UserEntity import User
from app.accessors import user_accessor
from app.managers.MessageManager import MessageManager

class AuthManager:
    def __init__(self):
        self.SCOPE = "user-read-private, user-read-email, user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public, streaming, app-remote-control, user-top-read"
        self.messageManager = MessageManager()

    def get_spotify_authorize_url(self, linking_url = None):
        sp_auth = spotipy.oauth2.SpotifyOAuth(scope = self.SCOPE, state=linking_url, show_dialog=True)
        return sp_auth.get_authorize_url()


    def handle_spotify_callback(self, code, linking_url = None):
        result = dict()
        sp_auth = spotipy.oauth2.SpotifyOAuth(scope = self.SCOPE, state=linking_url)
        token_object = sp_auth.get_access_token(code)

        #Token object is
        """
        access_token
        expires_at
        expires_in
        refresh_token
        scope
        token_type
        """
        access_token = token_object["access_token"]
        refresh_token = token_object["refresh_token"]
            
        spotify = spotipy.Spotify(auth=access_token) 
        current_user = spotify.current_user()
        # user object
        """
        spotify_id
        email
        display_name
        country
        """
        existing_user = user_accessor.get_user_by_email(current_user["email"])

        print(f'{current_user["email"]} is logging in')

        # If user email doesn't exist in our database
        # create the user
        if existing_user is None:
            print("creating user")
            new_user_object = User(current_user["id"], current_user["email"], current_user["display_name"], current_user["country"], origin="spotify", verified=1)
            user_accessor.insert(new_user_object)

        
        # add access token to auth table along with user info
        # NOTE: commented out because we probably don't need tokens to be saved in database
        # new_auth = Auth(current_user["email"], access_token, token_object["refresh_token"], "spotify", token_object["exipires_at"])
        # auth_accessor.insert(new_auth)

        result['email'] = current_user["email"]
        result['display_name'] = current_user["display_name"]
        result['id'] = 'empty'
        result['external_id'] = current_user["id"]
        result['access_token'] = access_token
        result['refresh_token'] = refresh_token
        result['product'] = current_user["product"]
        result['origin'] = "spotify"
        result['authenticated'] = True

        # return back to client the access_token and some basic info
        return result 

    def spotify_me(self, spt_token):
        try:
            result = dict()
            spotify = spotipy.Spotify(auth=spt_token) 
            current_user = spotify.me()

            # user object
            """
            spotify_id
            email
            display_name
            country
            """

            result['email'] = current_user["email"]
            result['display_name'] = current_user["display_name"]
            result['id'] = current_user["id"]
            result['authenticated'] = True

            return self.messageManager.getMessage(isError=False, message="User retrieved sucessfully", statusCode=200, data=result) 

        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 

    def refresh_token(self, refresh_token):
        try:
            sp_auth = spotipy.oauth2.SpotifyOAuth(scope = self.SCOPE)
            result = sp_auth.refresh_access_token(refresh_token)
            access_token = result["access_token"]
            print(f'server is sending back new token {access_token}')
            return self.messageManager.getMessage(isError=False, message="User retrieved sucessfully", statusCode=200, data=access_token) 

        except spotipy.exceptions.SpotifyException as err:
            return self.messageManager.getMessage(isError=True, message=err.msg, statusCode=err.http_status, data=None) 
