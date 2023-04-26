from flask import request
import json
from app import app
from app.managers.MessageManager import MessageManager
from app.managers.SpotifyManager import SpotifyManager
from app.middlewares.auth_middleware import require_authorization


messageManager = MessageManager()
spotify_manager = SpotifyManager() 


@app.route('/spotify/playlist/tracks', methods = ['POST'])
@require_authorization
def add_to_playlist(spt_token):

    # parse data from request body
    json_data = request.get_json(force=True)
    tracks = json_data["tracks"]
    playlist = json_data["playlist"]

    # Error checking
    if tracks is None:
        return messageManager.getMessage(isError=True, message="Missing tracks", statusCode=400, data=None)
    if not tracks:
        return messageManager.getMessage(isError=True, message="Tracks length is zero", statusCode=400, data=None)
    if playlist["id"] is None and playlist["name"] is None:
        return messageManager.getMessage(isError=True, message="Playlist needs to be specified", statusCode=400, data=None)

    # Send to add playlist
    return spotify_manager.addToPlaylist(spt_token, tracks, playlist)

@app.route('/spotify/playlists')
@require_authorization
def get_playlists(spt_token):

    return spotify_manager.getPlaylists(spt_token)

@app.route('/spotify/recommendations/initial')
@require_authorization
def get_recommendation(spt_token):
    genre_list = request.args.getlist('genre')
    print(genre_list)
    if len(genre_list) != 2:
        return messageManager.getMessage(isError=True, message="Missing genres", statusCode=400, data=None)
    
    return spotify_manager.getInitialRecommendation(token=spt_token, genres=genre_list)

# @app.route('/spotify/recommendations')
# @require_authorization
# def get_recommendation(spt_token):
#     genre_list = request.args.getlist('genre')
#     if len(genre_list) != 2:
#         return messageManager.getMessage(isError=True, message="Missing genres", statusCode=400, data=None)
    
#     # return spotify_manager.getRecommendations(token=spt_token, artists=artistList, genres=genre_list, tracks=tracksList)
#     return messageManager.getMessage(isError=True, message="Missing Maria DB", statusCode=404, data=None)

@app.route('/v2/spotify/recommendations/initial')
@require_authorization
def get_recommendations_v2(spt_token):
    return spotify_manager.get_recommendations_v2(spt_token)
