import requests
from wordpress.response import Response, MediaResponse


def upload_file_to_wordpress(file_name, wordpress_media_url, wordpress_header):
    image_name = file_name
    with open(image_name, 'rb') as img:
        payload = {}
        files = [('media', (image_name, img, 'application/octet-stream'))]

        response = Response(requests.post(wordpress_media_url, data=payload, files=files, headers=wordpress_header))
        if response.is_successful():
            return response.image_location
        else:
            return None


def upload_to_wordpress(file_names, wordpress_media_url, wordpress_header):
    images = []
    for file_name in file_names:
        images.append(upload_file_to_wordpress(file_name, wordpress_media_url, wordpress_header))

    return images


def get_wordpress_media(wordpress_get_media_url, wordpress_header):
    response = MediaResponse(requests.get(wordpress_get_media_url, headers=wordpress_header))
    return response
