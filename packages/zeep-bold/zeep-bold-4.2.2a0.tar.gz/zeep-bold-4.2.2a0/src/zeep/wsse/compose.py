class Compose:
    def __init__(self, wsse_objects):
        self.wsse_objects = wsse_objects

    def apply(self, envelope, headers):
        for obj in self.wsse_objects:
            envelope, headers = obj.apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):
        for obj in self.wsse_objects:
            obj.verify(envelope)

    def verify_response(self, envelope):
        for obj in self.wsse_objects:
            obj.verify_response(envelope)
