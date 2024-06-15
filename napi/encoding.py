import locale
from typing import Optional, Tuple

import chardet

DECODING_ORDER = ["utf-16", "windows-1250", "windows-1251", "windows-1252", "windows-1253", "windows-1254", "utf-8"]
CHECK_NUM_CHARS = 5000
AUTO_DETECT_THRESHOLD = 0.9


def _is_ascii(c: str) -> bool:
    return ord(c) < 128


def _is_polish_diacritic(c: str) -> bool:
    return c in "ąćęłńóśżźĄĆĘŁŃÓŚŻŹ"


def _is_correct_encoding(subs: str) -> bool:
    err_symbols, diacritics = 0, 0
    for char in subs[:CHECK_NUM_CHARS]:
        if _is_polish_diacritic(char):
            diacritics += 1
        elif not _is_ascii(char):
            err_symbols += 1

    return err_symbols < diacritics


def _detect_encoding(subs: bytes) -> Tuple[Optional[str], float]:
    result = chardet.detect(subs)
    return result["encoding"], result["confidence"]


def _try_decode(subs: bytes) -> Tuple[str, str]:
    encoding, confidence = _detect_encoding(subs)
    if encoding and confidence > AUTO_DETECT_THRESHOLD:
        try:
            return encoding, subs.decode(encoding)
        except UnicodeDecodeError:
            pass

    last_exc = None
    for i, enc in enumerate(DECODING_ORDER):
        try:
            encoded_subs = subs.decode(enc)
            if _is_correct_encoding(encoded_subs):
                return enc, encoded_subs
        except UnicodeDecodeError as e:
            last_exc = e
    raise ValueError("Could not encode using any of {}: {}".format(DECODING_ORDER, last_exc))


def decode_subs(subtitles_binary: bytes, use_enc: Optional[str] = None) -> Tuple[str, str]:
    if use_enc is not None:
        return use_enc, subtitles_binary.decode(use_enc)
    else:
        return _try_decode(subtitles_binary)


def encode_subs(subs: str) -> Tuple[str, bytes]:
    target_encoding = locale.getpreferredencoding()
    return target_encoding, subs.encode(target_encoding)
