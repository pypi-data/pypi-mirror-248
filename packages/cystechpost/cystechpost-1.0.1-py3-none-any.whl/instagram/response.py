import json


class Response:
    def __init__(self, response):
        self.text = response.text
        self.json = json.loads(self.text)
        self.creation_id = self.creation_id()

    def creation_id(self):
        if 'id' in self.json:
            return int(self.json['id'])
        else:
            return None
