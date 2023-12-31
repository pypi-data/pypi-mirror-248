import requests

from instagram import GRAPH_MEDIA_URL, GRAPH_MEDIA_PUBLISH_URL, TEST_IMAGE_LOCATION, TEST_CAPTION, CAROUSEL_MEDIA_TYPE
from instagram.response import Response


def create_test_post(instagram_page_id, graph_api_token):
    media_url = GRAPH_MEDIA_URL.format(instagram_page_id)
    media_payload = {
        'image_url': TEST_IMAGE_LOCATION,
        'caption': TEST_CAPTION,
        'access_token': graph_api_token
    }
    response = Response(requests.post(media_url, data=media_payload))

    if response.creation_id is not None:
        creation_id = response.creation_id

        publish_url = GRAPH_MEDIA_PUBLISH_URL.format(instagram_page_id)
        publish_payload = {
            'creation_id': creation_id,
            'access_token': graph_api_token
        }
        response = Response(requests.post(publish_url, data=publish_payload))
        return response.creation_id
    else:
        return False


def create_post(instagram_page_id, graph_api_token, image_location, caption):
    media_url = GRAPH_MEDIA_URL.format(instagram_page_id)
    media_payload = {
        'image_url': image_location,
        'caption': caption,
        'access_token': graph_api_token
    }
    response = Response(requests.post(media_url, data=media_payload))

    if response.creation_id is not None:
        creation_id = response.creation_id

        publish_url = GRAPH_MEDIA_PUBLISH_URL.format(instagram_page_id)
        publish_payload = {
            'creation_id': creation_id,
            'access_token': graph_api_token
        }
        response = Response(requests.post(publish_url, data=publish_payload))
        return response.creation_id
    else:
        return False


def create_carousel(instagram_page_id, graph_api_token, image_locations, caption):
    post_url = GRAPH_MEDIA_URL.format(instagram_page_id)
    media_publish_url = GRAPH_MEDIA_PUBLISH_URL.format(instagram_page_id)

    carousel_post_ids = []

    for image_location in image_locations:
        payload = {
            'image_url': image_location,
            'is_carousel_item': True,
            'access_token': graph_api_token
        }

        request = Response(requests.post(post_url, params=payload))
        container_id = request.creation_id
        carousel_post_ids.append(container_id)

    carousel_payload = {
        'media_type': CAROUSEL_MEDIA_TYPE,
        'caption': caption,
        'children': carousel_post_ids,
        'access_token': graph_api_token
    }

    carousel_response = Response(requests.post(post_url, json=carousel_payload))
    creation_id = carousel_response.creation_id

    publish_payload = {
        'creation_id': creation_id,
        'access_token': graph_api_token
    }

    publish_id = Response(requests.post(media_publish_url, params=publish_payload)).creation_id
    return publish_id
