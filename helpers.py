import re

def sanitize_name(name):
    """Removes illegal characters that Windows forbids in folder and file names."""
    sanitized = re.sub(r'[<>:"/\\|?*]', '', str(name))
    return sanitized.strip(' .')

def get_primary_artist(artist_string):
    """Splits concatenated artist strings and returns on the primary artist"""
    artist_string = str(artist_string)
    parts = re.split(r'(?i)\s*(?:;|\bfeat\.?\b|\bft\.?\b)', str(artist_string))

    return parts[0].strip()




# Format
class formatText:
    """Allows text to be formatted with different colours"""

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