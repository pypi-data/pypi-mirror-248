import zipfile
import os
from typing import Optional

import requests

def _create_unzip_folder(path: str) -> bool:
    try:
        os.mkdir(path = path)
        return True
    except Exception:
        return False

def unzip(zip_path: str, target_path: str) -> Optional[Exception]:
    is_successful: bool = _create_unzip_folder(path = target_path)
    if is_successful == False:
        return Exception("failed to create unzip folder")
    
    try:
        with zipfile.ZipFile(file = zip_path, mode = "r") as zip_ref:
            zip_ref.extractall(path = target_path)
    except Exception as unzip_err:
        return Exception(
            f"failed to extract zip file contents to target path; {unzip_err.args}"
        )
    return None

def download_zip(
    url: str, 
    file_path: str, 
    chunk_size: int = 128
) -> Optional[Exception]:
    res: requests.Response = requests.get(url = url, stream = True)
    if res.status_code > 200:
        return Exception(f'failed to GET from "{url}"')
    try:
        with open(file = file_path, mode = 'wb') as file_download:
            for chunk in res.iter_content(chunk_size = chunk_size):
                file_download.write(chunk)
    except Exception as write_err:
        return Exception(f'failed to write zip file to "{file_path}"; {write_err.args}')
    return None