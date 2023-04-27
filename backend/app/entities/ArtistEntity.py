class Artist:
    def __init__(self, id, artist_name, href,origin, uri = None, pk = None):
        self.id = id
        self.artist_name = artist_name
        self.href = href
        self.uri = uri
        self.pk = pk
        self.origin = origin
