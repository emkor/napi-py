import locale
from typing import Optional, Tuple
import chardet

DECODING_ORDER = ["utf-8-sig", "utf-16", "windows-1250", "windows-1251", "windows-1252", "windows-1253", "windows-1254", "utf-8"]
CHECK_NUM_CHARS = 5000
AUTO_DETECT_THRESHOLD = 0.9

def _is_ascii(c: str) -> bool:
    return ord(c) < 128

def _is_polish_diacritic(c: str) -> bool:
    return c in "ąćęłńóśżźĄĆĘŁŃÓŚŻŹ"

def _is_correct_encoding(subs: str) -> bool:
    if not subs:
        return False
    err_symbols, diacritics = 0, 0
    for char in subs[:CHECK_NUM_CHARS]:
        if _is_polish_diacritic(char):
            diacritics += 1
        elif not _is_ascii(char):
            err_symbols += 1

    return diacritics > 0 and err_symbols <= diacritics

def _detect_encoding(subs: bytes) -> Tuple[Optional[str], float]:
    try:
        result = chardet.detect(subs)
        return result["encoding"], result["confidence"]
    except Exception:
        return None, 0.0

def _try_decode(subs: bytes) -> Tuple[str, str]:
    encoding, confidence = _detect_encoding(subs)
    if encoding and confidence > AUTO_DETECT_THRESHOLD:
        try:
            actual_enc = "utf-8-sig" if encoding.lower() == "utf-8" else encoding
            return actual_enc, subs.decode(actual_enc)
        except (UnicodeDecodeError, LookupError):
            pass

    last_exc = None
    for enc in DECODING_ORDER:
        try:
            decoded_subs = subs.decode(enc)
            if _is_correct_encoding(decoded_subs):
                return enc, decoded_subs
        except (UnicodeDecodeError, LookupError) as e:
            last_exc = e
            continue

    try:
        return "utf-8", subs.decode("utf-8", errors="replace")
    except Exception:
        raise ValueError(f"Could not decode using any of {DECODING_ORDER}. Last error: {last_exc}")

def decode_subs(subtitles_binary: bytes, use_enc: Optional[str] = None) -> Tuple[str, str]:
    if use_enc is not None:
        try:
            return use_enc, subtitles_binary.decode(use_enc)
        except UnicodeDecodeError:
            return _try_decode(subtitles_binary)
    else:
        return _try_decode(subtitles_binary)

def encode_subs(subs: str) -> Tuple[str, bytes]:
    target_encoding = locale.getpreferredencoding(False) or "utf-8"
    try:
        return target_encoding, subs.encode(target_encoding)
    except UnicodeEncodeError:
        return "utf-8", subs.encode("utf-8")
