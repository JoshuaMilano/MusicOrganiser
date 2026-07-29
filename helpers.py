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