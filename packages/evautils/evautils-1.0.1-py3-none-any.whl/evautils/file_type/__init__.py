import os
import filetype


def is_file(file_path: str) -> bool:
    return bool(file_path and os.path.isfile(file_path))


def is_directory(directory_path: str) -> bool:
    return bool(directory_path and os.path.isdir(directory_path))


def is_image(image_path: str) -> bool:
    if is_file(image_path):
        mimetype = filetype.guess(image_path).mime
        return bool(mimetype and mimetype.startswith('image/'))
    return False


def is_video(video_path: str) -> bool:
    if is_file(video_path):
        mimetype = filetype.guess(video_path).mime
        return bool(mimetype and mimetype.startswith('video/'))
    return False
