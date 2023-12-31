# You will need to setup your own images directory to test the uploads.
# Just as well, you will need to input your own Wordpress credentials here to test the WordPress functions.
EXTERNAL_IMAGES_DIRECTORY = "../../Path/To/Dir/"
EXTERNAL_IMAGE = "../../Path/To/Dir/Picture.JPG"
WORDPRESS_MEDIA_URL = "https://public-api.wordpress.com/rest/v1.1/sites/yoursite/media/new"
WORDPRESS_GET_MEDIA_URL="https://public-api.wordpress.com/rest/v1.1/sites/yoursite/media/"
WORDPRESS_ACCESS_TOKEN = 'LoremIpsumDolorEt'
WORDPRESS_HEADER = {'Authorization': f'BEARER {WORDPRESS_ACCESS_TOKEN}'}