# CYSTech Post (POST) V1.0
### Social Media Content Planning and Publishing Library

## Introduction
This is the custom in-house Instagram content planning and publishing library for CYSTech + CYS Special Projects.

This has been built from the now deprecated/defunct code used in CYSTech Planner (PLNR)

## Project Structure
Unlike the CLI version of this tool (PLNR), this project structure is a bit more simple.

```
/POST
    |-instagram
        |-instagram_service.py
        |-response.py
    |-system
        |-file_dialog.py
    |-tests
        |-test_file_dialog.py
        |-test_instagram_service.py
        |-test_wordpress_service.py
    |-wordpress
        |-instagram_service.py
        |-response.py
    |-README.md
    |-setup.py
```
Every package has an `__init__.py`.

## Getting Started
This is not a proper app itself, but rather a package/library of simple functions to upload and publish content/media to various social media outlets.

The initial function and purpose of this library is to be able to neatly and uniformly upload media to the Clean Your Shoes website (currently being hosted on WordPress), and then use that now hosted media as content to publish to Instagram.

However, due to how the methods are built out, this allows for anyone to set up content to their proper WordPress website, as well as allowing users to publish content to their Instagram page that may be hosted elsewhere (WordPress is just where CYS keeps public media).

## Testing
We have our tests in the `tests/` folder. To run the whole suite, you can simply run:

```python -m pytest tests/``` or ```python setup.py pytest ```

For individual testing, simply add the test file at the end of the `tests/` directory.

At present, all tests will automatically fail because they require sensitive credentials/information to test the functions. You will need to input your own credentials for each service in their respective `__init__.py` files and in `tests/__init__.py`

## Features
This library allows you to do the following:
- Upload media to WordPress.
- Publish content to Instagram.
- Search and select files to upload.

## Library Publishing
As we improve upon this library, we will want to update the latest publicly available package. After a new update/revision:

Make sure your present working directory is `/path/to/POST` (so the root folder). In your command prompt, run:

    % python setup.py bdist_wheel

The wheel file is stored in the `dist` folder that is now created. You can install the library by using:

    % pip install /path/to/wheelfile.whl

Note that you could also publish your library to the official PyPI repository and install it from there (recommended).

Once you have installed your Python library, you can import it using:

    import mypythonlib
    from mypythonlib import myfunctions
