from flask import jsonify
class MessageManager:
    def __init__(self):
        pass
    
    def getMessage(self, isError=None, message=None, statusCode=None, data=None):
        if isError is None and message is None and statusCode is None and data is None:
            return jsonify(isError=True, message="None Error", statusCode=500, data=""), 500
        else:
            if isError is None:
                isError = False
            if message is None:
                message = ""
            if statusCode is None:
                statusCode = 200
            if data is None:
                data = ""
            return jsonify(isError=isError, message=str(message), statusCode= statusCode, data=data), statusCode
