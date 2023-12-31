from errors import ERRORS, WP_UPLOAD_ERROR


class Response:
    def __init__(self, response):
        self.json = response.json()
        self.media = self.json["media"][0]
        self.upload_id = self.media['ID']
        self.image_location = self.media['URL']

    def is_successful(self):
        if isinstance(self.upload_id, int) and self.upload_id > 0:
            return True
        else:
            print(ERRORS.get(WP_UPLOAD_ERROR))
            return False


class MediaResponse:
    def __init__(self, response):
        self.json = response.json()
        self.media = self.json["media"]
        self.media_list = self.create_media_list()

    def create_media_list(self):
        media_list = []
        for m in self.media:
            media_object = Media(m)
            media_list.append(media_object)

        return media_list


class Media:
    def __init__(self, media):
        self.id = media['ID']
        self.filename = media['file']
        self.url = media['URL']
