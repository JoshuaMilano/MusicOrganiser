import re, mutagen, shutil
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SongMetadata:
    """data class to track music metadata"""
    title: str
    artist: str
    album: str
    album_artist: str

def get_song_metadata(file_path):
    """Extracts tags from an audio file"""
    try:
        audio = mutagen.File(file_path, easy=True)
    except TypeError:
        audio = mutagen.File(file_path)

    if audio is None:
        print(FormatText.info(f'[{file_path.name}]: No readable tags found!'))
        return None

    raw_title = audio.get('title', [file_path.stem])[0]
    raw_artist = get_primary_artist(audio.get('artist', ['Unknown Artist'])[0])
    raw_album = audio.get('album', ['Unknown Album'])[0]
    raw_album_artist = get_primary_artist((audio.get('albumartist') or audio.get('artist', ['Unknown Artist']))[0])

    return SongMetadata(
        title = sanitise_data(raw_title),
        artist = sanitise_data(raw_artist),
        album = sanitise_data(raw_album),
        album_artist = sanitise_data(raw_album_artist)
    )


def sanitise_data(name):
    """Removes illegal characters that Windows forbids in folder and file names."""
    sanitised = re.sub(r'[<>:"/\\|?*]', '', str(name))
    return sanitised.strip(' .')

def get_primary_artist(artist_string):
    """Splits concatenated artist strings and returns on the primary artist."""
    artist_string = str(artist_string)
    parts = re.split(r'(?i)\s*(?:;|\bfeat\.?\b|\bft\.?\b)', str(artist_string))

    return parts[0].strip()

def copy_album_img(
        original_album_folder: Path,
        target_album_folder: Path,
        allowed_extensions: set
    ):
    """Copies album art from the original location to the new location if that album art image extension is allowed"""

    images_in_folder = [img for img in original_album_folder.iterdir() if img.suffix.lower() in allowed_extensions]

    if images_in_folder:
        cover_source = images_in_folder[0]
        cover_target = target_album_folder / f'cover{cover_source.suffix.lower()}'

        if not cover_target.exists():
            shutil.copy2(cover_source, cover_target)
            return 'COPIED' # Copied album art
        
        return 'EXISTS' # album_art already exists

    return 'MISSING' # No images in folder

def get_artist_img():
    pass

# Format
class FormatText:
    """Allows text to be formatted with different colours."""

    ERROR = '\033[31m' # RED
    SUCCESS = '\033[32m' # GREEN
    ALERT = '\033[33m' # YELLOW
    INFO = '\033[34m' # BLUE
    RESET = '\033[0m' # RESET TEXT

    # Method definitions
    @classmethod
    def error(cls, message):
        """Formats the terminal text as RED"""
        return f'{cls.ERROR}{message}{cls.RESET}'

    @classmethod
    def success(cls, message):
        """Formats the terminal text as GREEN"""
        return f'{cls.SUCCESS}{message}{cls.RESET}'

    @classmethod
    def alert(cls, message):
        """Formats the terminal text as YELLOW"""
        return f'{cls.ALERT}{message}{cls.RESET}'

    @classmethod
    def info(cls, message):
        """Formats the terminal text as BLUE"""
        return f'{cls.INFO}{message}{cls.RESET}'