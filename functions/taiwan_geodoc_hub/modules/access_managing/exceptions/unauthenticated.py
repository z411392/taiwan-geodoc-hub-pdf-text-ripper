class Unauthenticated(Exception):
    def __init__(self):
        pass

    def __iter__(self):
        yield "type", __class__.__name__
