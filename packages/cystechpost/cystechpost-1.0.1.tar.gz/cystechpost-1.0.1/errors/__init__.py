(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    IG_ERROR,
    WP_ERROR,
    WP_UPLOAD_ERROR
) = range(9)

ERRORS = {
    DIR_ERROR: "Config directory error",
    FILE_ERROR: "Config file error",
    DB_READ_ERROR: "Database read error",
    DB_WRITE_ERROR: "Database write error",
    IG_ERROR: "Instagram post error",
    WP_ERROR: "WordPress post error",
    WP_UPLOAD_ERROR: "There was an error uploading the data. Please check CLI output below:",
}