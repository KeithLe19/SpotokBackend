from flask import redirect, request
from app import app
from app.managers.MessageManager import MessageManager
from app.managers.AuthManager import AuthManager
from app.middlewares.auth_middleware import require_authorization

# Don't reuse a auth_manager object because they store token info and you could leak user tokens if you reuse a auth_manager object

messageManager = MessageManager()



@app.route("/login/spotify")
def login_with_spotify():
    linking_url = request.args.get('linkingUrl')
    # initialize auth_manager
    auth_manager = AuthManager()
    # get auth url
    auth_url = auth_manager.get_spotify_authorize_url(linking_url)
    # redirect to auth_url
    return redirect(f'{auth_url}')


@app.route("/callback/spotify")
def spotify_callback():
    # get code from query
    code = request.args.get('code')
    linking_url = request.args.get('state')

    if linking_url is not None:
        return redirect(f'{linking_url}?code={code}')

    # # initialize auth_manager
    auth_manager = AuthManager()
    user_auth = auth_manager.handle_spotify_callback(code, linking_url)
    
    
    return messageManager.getMessage(isError=False, message="Authenticated successfully", statusCode=200, data=user_auth)


@app.route('/spotify/me')
@require_authorization
def me(spt_token):
    # initialize auth_manager
    auth_manager = AuthManager()

    return auth_manager.spotify_me(spt_token)

@app.route('/token/refresh/spotify', methods=["POST"])
def refresh_token():

    # parse data from request body
    json_data = request.get_json(force=True)
    refresh_token = json_data["refreshToken"]
    print("refresh token found")
    print(refresh_token)

    # initialize auth_manager
    auth_manager = AuthManager()

    return auth_manager.refresh_token(refresh_token)

