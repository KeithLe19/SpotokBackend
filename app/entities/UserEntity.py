class User:
    def __init__(self, id, email, display_name, country, origin, verified = 0, phone = None, pk = None):
        self.id = id
        self.email = email
        self.display_name = display_name
        self.country = country
        self.phone = phone
        self.verified = verified
        self.pk = pk
        self.origin = origin
