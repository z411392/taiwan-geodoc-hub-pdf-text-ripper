class InvalidPDF(Exception):
    def __iter__(self):
        yield "type", __class__.__name__
