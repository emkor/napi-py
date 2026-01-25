from io import BytesIO
from typing import Optional, Dict
import threading
import py7zr

NAPI_ARCHIVE_PASSWORD = "iBlm8NTigvru0Jr0"


class InMemoryIO(py7zr.io.Py7zIO):
    def __init__(self, fname: str):
        self.fname = fname
        self._buf = bytearray()
        self._length = 0
        self._lock = threading.Lock()

    def write(self, data: bytes) -> int:
        with self._lock:
            self._buf.extend(data)
            self._length += len(data)
            return len(data)

    def read(self, size: Optional[int] = None) -> bytes:
        return b""

    def seek(self, offset: int, whence: int = 0) -> int:
        return offset

    def flush(self) -> None:
        pass

    def size(self) -> int:
        return self._length

    def getvalue(self) -> bytes:
        with self._lock:
            return bytes(self._buf)


class InMemoryFactory(py7zr.io.WriterFactory):
    def __init__(self, target_filename: Optional[str] = None):
        self.products: Dict[str, InMemoryIO] = {}
        self.target_filename = target_filename

    def create(self, filename: str) -> py7zr.io.Py7zIO:
        if self.target_filename is not None and filename != self.target_filename:
            product = InMemoryIO(filename)
        else:
            product = InMemoryIO(filename)
            self.products[filename] = product
        return product


def un7zip_api_response(content_7z: bytes, target_filename: Optional[str] = None) -> Optional[bytes]:
    try:
        buffer = BytesIO(content_7z)
        with py7zr.SevenZipFile(buffer, mode="r", password=NAPI_ARCHIVE_PASSWORD) as archive:
            factory = InMemoryFactory(target_filename=target_filename)
            archive.extractall(factory=factory)

        if target_filename:
            product = factory.products.get(target_filename)
            return product.getvalue() if product else None

        if not factory.products:
            return None
        first_product = next(iter(factory.products.values()))
        return first_product.getvalue()

    except py7zr.exceptions.UnsupportedCompressionMethodError:
        if content_7z and (b"1\r\n" in content_7z or b"00:00:" in content_7z or b"{" in content_7z):
            return content_7z
        return None
    except (py7zr.exceptions.Bad7zFile, py7zr.exceptions.PasswordRequired):
        return None
