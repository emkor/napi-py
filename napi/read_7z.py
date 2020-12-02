from io import BytesIO
from typing import Optional
from py7zlib import Archive7z, ArchiveError

NAPI_ARCHIVE_PASSWORD = "iBlm8NTigvru0Jr0"


def un7zip_api_response(content_7z: bytes) -> Optional[bytes]:
    try:
        buffer = BytesIO(content_7z)
        archive = Archive7z(buffer, password=NAPI_ARCHIVE_PASSWORD)
        return archive.getmember(0).read()
    except ArchiveError:
        return None
