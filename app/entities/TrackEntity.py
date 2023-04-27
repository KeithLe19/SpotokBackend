class Track:
    def __init__(self, id, track_name, href, duration_ms, origin, uri = None, catchy_start = None, pk = None):
        self.id = id
        self.track_name = track_name
        self.href = href
        self.duration_ms = duration_ms
        self.uri = uri
        self.catchy_start = catchy_start
        self.pk = pk
        self.origin = origin
