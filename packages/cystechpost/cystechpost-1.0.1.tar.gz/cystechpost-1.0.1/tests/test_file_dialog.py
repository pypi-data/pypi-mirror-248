from system.file_dialog import select_files


def test_select_file():
    # There will be a better way to test this, but for now, if it opens and selects a file, it works.
    result = select_files()
    assert result is not None
