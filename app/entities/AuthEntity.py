class Auth:
    def __init__(self, email, access_token, refresh_token, auth_type, expires_at, pk = None):
        self.email = email
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.auth_type = auth_type
        self.expires_at = expires_at
        self.pk = pk
