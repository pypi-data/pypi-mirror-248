from instagram import TEST_IMAGE_LOCATION, TEST_CAPTION
from instagram.instagram_service import create_test_post, create_carousel, create_post
from tests import GRAPH_API_TOKEN, INSTAGRAM_PAGE_ID


def test_create_instagram_test_post():
    graph_api_token = GRAPH_API_TOKEN
    instagram_page_id = INSTAGRAM_PAGE_ID

    # Since we realistically cannot predict what the id will be, we just need to test for a number.
    assert create_test_post(instagram_page_id, graph_api_token) > 0


def test_create_post():
    graph_api_token = GRAPH_API_TOKEN
    instagram_page_id = INSTAGRAM_PAGE_ID
    image_location = TEST_IMAGE_LOCATION
    caption = TEST_CAPTION

    assert create_post(instagram_page_id, graph_api_token, image_location, caption) > 0


def test_create_carousel():
    graph_api_token = GRAPH_API_TOKEN
    instagram_page_id = INSTAGRAM_PAGE_ID
    image_locations = [TEST_IMAGE_LOCATION, TEST_IMAGE_LOCATION]
    caption = TEST_CAPTION

    assert create_carousel(instagram_page_id, graph_api_token, image_locations, caption) > 0
