
class Asset:

    def __init__(self, path, mimetype, start_location, end_location, flags):
        self.path = path
        self.mimetype = mimetype
        self.start_location = start_location
        self.end_location = end_location
        self.flags = flags

    @staticmethod
    def from_string(string):
        path, data = string.split(": ", 1)
        data = str.split(data.rstrip(), " ")
        asset = Asset(path, data[0], int(data[1]), int(data[2]), data[3:])
        return asset

    def __str__(self) -> str:
        return str.format("{}: {} {} {} {}", self.path, self.mimetype, self.start_location, self.end_location,  str.join(" ", self.flags))
