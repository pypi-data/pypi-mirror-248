from system.file_dialog import select_files
from wordpress import WORDPRESS_MEDIA_URL, WORDPRESS_HEADER, WORDPRESS_GET_MEDIA_URL
from wordpress.wordpress_service import upload_file_to_wordpress, upload_to_wordpress, get_wordpress_media


def test_upload_file_to_wordpress():
    file_name = select_files()[0]
    wordpress_media_url = WORDPRESS_MEDIA_URL
    wordpress_header = WORDPRESS_HEADER

    result = upload_file_to_wordpress(file_name, wordpress_media_url, wordpress_header)
    assert result is not None


def test_upload_to_wordpress():
    file_names = select_files()
    wordpress_media_url = WORDPRESS_MEDIA_URL
    wordpress_header = WORDPRESS_HEADER

    result = upload_to_wordpress(file_names, wordpress_media_url, wordpress_header)
    assert result is not None


def test_get_wordpress_media():
    wordpress_get_media_url = WORDPRESS_GET_MEDIA_URL
    wordpress_header = WORDPRESS_HEADER

    result = get_wordpress_media(wordpress_get_media_url, wordpress_header)
    assert len(result.media_list) >= 1
