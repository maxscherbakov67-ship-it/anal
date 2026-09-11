import os
from bot.handlers.commands import audio_path
from utils.exceptions import filesizeError
import logging
MAX_FILESIZE = 20
EXTENSION_LIST = [".mp3", ".wav", ".flac", ".aac"]
FORMAT_LIST = ["mp3", "flac", "wav"]

logging.basicConfig(level=logging.INFO, filename="errors.log", filemode="a",
                    format="%(name)s%(asctime)s %(levelname)s %(message)s")
def get_size_mb():
    size_bytes = os.path.getsize(audio_path)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb
def get_extension():
    extension = os.path.splitext(audio_path)[1].lower()
    return extension
def approve_size():
    if get_size_mb() <= MAX_FILESIZE:
        return True
    else: return False
def approve_format():
    if get_extension() in EXTENSION_LIST:
        return True
    else: return False
def approve_format_bytes(audio_path):
    with open(audio_path, "rb") as f:
        header = f.read(12)
    if header.startswith(b"ID3"):
        format = "mp3"
        return format
    elif header.startswith(b"fLaC"):
        format = "flac"
        return format
    elif header.startswith(b"RIFF") and header[8:12] == b"WAVE":
        format = "wav"
        return format
    elif header[0] == 0xFF and (header[1] & 0xE0) == 0xE0:
        format = "mp3"
        return format
    else:
        format = None
        return format
def validate_audio_file(audio_path: str) -> dict:
    result = {}
    if approve_size() == True:
        result["ok"] = True
        result["error"] = None
    else: 
        result["ok"] = False
        result["error"] = "file_too_large"
    if approve_format() == True:
        result["ok"] = True
        result["error"] = None
    else:
        result["ok"] = False
        result["error"] = "wrong_format"
    if approve_format_bytes(audio_path) in FORMAT_LIST:
        result["ok"] = True
        result["error"] = None
    else:
        result["ok"] = False
        result["error"] = "validation_format_error"
    return result