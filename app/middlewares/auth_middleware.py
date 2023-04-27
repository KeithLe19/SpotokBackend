from functools import wraps
from flask import request
from app.managers.MessageManager import MessageManager

message_manager = MessageManager()


def require_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        spt_token = None
        if "Authorization" in request.headers:
            spt_token = request.headers["Authorization"].split(" ")[1]
            print(f"found token in header: {spt_token}")
            return f(spt_token, *args, **kwargs)
        else:
            print("No authorization token found")
            return message_manager.getMessage(isError=True, message="Unauthorized", statusCode=401, data=None) 
    return decorated
