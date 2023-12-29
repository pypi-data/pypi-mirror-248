import os
import requests
import subprocess
from typing import List
from functools import lru_cache
from ..file_type import is_file
from concurrent.futures import ThreadPoolExecutor


def download_file(download_directory_path: str, url: str) -> str:
    download_file_path = os.path.join(
        download_directory_path,
        os.path.basename(url)
    )
    total = get_download_size(url)
    if is_file(download_file_path):
        initial = os.path.getsize(download_file_path)
    else:
        initial = 0
    if initial < total:
        subprocess.Popen(['curl', '--create-dirs', '--silent', '--insecure',
                          '--location', '--continue-at', '-', '--output', download_file_path, url])

    return download_file_path


def conditional_download(download_directory_path: str, urls: List[str]) -> None:
    with ThreadPoolExecutor() as executor:
        for url in urls:
            executor.submit(download_file, download_directory_path, url)


@lru_cache(maxsize=None)
def get_download_size(url: str) -> int:
    try:
        response = requests.get(url, timeout=10)
        return int(response.headers.get('Content-Length'))
    except (OSError, ValueError):
        return 0


def is_download_done(url: str, file_path: str) -> bool:
    if is_file(file_path):
        return get_download_size(url) == os.path.getsize(file_path)
    return False
