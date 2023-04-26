from flask import request
from app import app
from app.managers.MessageManager import MessageManager
from app.managers.SpotokManager import SpotokManager
from app.middlewares.auth_middleware import require_authorization


messageManager = MessageManager()
spotok_manager = SpotokManager() 

@app.route("/")
def index():
    return messageManager.getMessage(isError=False, message="Success", statusCode=200, data="Hello App")


@app.route("/genres")
def get_spotok_available_genre():
    return spotok_manager.get_all_genres()

@app.route("/genres/me")
@require_authorization
def get_user_genres(spt_token):
    return spotok_manager.get_user_genres(spt_token)

@app.route("/genre", methods=["POST"])
@require_authorization
def add_user_genre(spt_token):
    json_data = request.get_json(force=True)
    genre_ids = json_data["genreIds"]
    return spotok_manager.insert_user_genre(spt_token, genre_ids)

@app.route("/library/tracks")
@require_authorization
def get_user_tracks_library(spt_token):
    return spotok_manager.get_user_library(spt_token)

@app.route("/library/tracks/<track_id>", methods=["DELETE"])
@require_authorization
def remove_track_from_user_library(spt_token, track_id):
    return spotok_manager.remove_track_from_user_library(spt_token, track_id)

@app.route("/library/tracks", methods=["POST"])
@require_authorization
def add_track_to_user_library(spt_token):
    print("library/tracks is called")

    # parse data from request body
    json_data = request.get_json(force=True)
    track_id = json_data["trackExternalId"]

    return spotok_manager.add_track_to_user_library(spt_token, track_id)

