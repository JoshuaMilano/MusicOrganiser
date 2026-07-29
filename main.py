from pathlib import Path
import time
import mutagen
import shutil

from helpers import sanitize_name, get_primary_artist



ERROR = '\033[31m' # RED
SUCCESS = '\033[32m' # GREEN
ALERT = '\033[33m' # YELLOW
INFO = '\033[34m' # BLUE
RESET = '\033[0m' # Plain TExt


def organise_directory(source_path, target_path):
    source_dir = Path(source_path)
    target_dir = Path(target_path)

    target_dir.mkdir(parents=True, exist_ok=True)

    # Supported music file extensions
    supported_music_extensions = {'.flac', '.mp3', '.wav'}
    # Supported image file extensions (For artists and album art)
    supported_image_extensions = {'.jpg', '.jpeg', '.png'}

    # append f (file) for every f (file) in source_dir.rglob('*') if the file suffix converted to lowercase is in the supported music extensions
    # .rglob will recursively search the entire source directory.
    audio_files = [f for f in source_dir.rglob('*') if f.suffix.lower() in supported_music_extensions]
    song_count = len(audio_files)

    # Set to store the PATH of albums we've found
    processed_albums = set()
    # Set to store the PATH of the artists we've found.
    processed_artists = set()

    print(f'Found {INFO}{len(audio_files)} {RESET}audio files. Reading Metadata...\n')
    print('-' * 40)

    for index, file_path in enumerate(audio_files, 1):
        try:
            try:
                audio = mutagen.File(file_path, easy=True)
            except TypeError:
                audio = mutagen.File(file_path)
                

            if audio is None:
                print(f'[{file_path.name}] -> No readable tags found!')
                print('-' * 40)
                continue

            raw_artist = audio.get('artist', ['Unknown Artist'])[0]
            raw_album = audio.get('album', ['Unkown Album'])[0]
            album_artist_list = audio.get('albumartist') or audio.get('artist', ['Unknown Artist'])
            raw_album_artist = album_artist_list[0]
            raw_title = audio.get('title', [file_path.stem])[0]

            primary_artist = get_primary_artist(raw_artist)
            primary_album_artist = get_primary_artist(raw_album_artist)

            safe_artist = sanitize_name(primary_artist)
            safe_album = sanitize_name(raw_album)
            safe_album_artist = sanitize_name(primary_album_artist)
            safe_title = sanitize_name(raw_title)

            artist_folder = target_dir / safe_album_artist
            new_folder = target_dir / safe_album_artist / safe_album
            new_folder.mkdir(parents=True, exist_ok=True)

            new_file_path = new_folder / f'{safe_title}{file_path.suffix.lower()}'

            if artist_folder not in processed_artists:
                original_folder = file_path.parent
                artist_img_source = None

                for ext in supported_image_extensions:
                    if (original_folder / f'artist{ext}').exists():
                        artist_img_source = original_folder / f'artist{ext}'
                        break
                    elif (original_folder.parent / f'artist{ext}').exists():
                        artist_img_source = original_folder.parent / f'artist{ext}'
                        break

                if artist_img_source:
                    artist_img_target = artist_folder / f'artist{artist_img_source.suffix.lower()}'
                    if not artist_img_target.exists():
                        shutil.copy2(artist_img_source, artist_img_target)
                        print(f'{SUCCESS}COPIED ARTIST PIC: {safe_album_artist}')

                processed_artists.add(artist_folder)

            if new_folder not in processed_albums:
                original_folder = file_path.parent

                images_in_folder = [img for img in original_folder.iterdir() if img.suffix.lower() in supported_image_extensions]

                if images_in_folder:
                    cover_source = images_in_folder[0]
                    cover_target = new_folder / f'cover{cover_source.suffix.lower()}'

                    if not cover_target.exists():
                        shutil.copy2(cover_source, cover_target)
                        print(f'{SUCCESS}COPIED ALBUM ART: {safe_album}')

                processed_albums.add(new_folder)

            if not new_file_path.exists():
                shutil.copy2(file_path, new_file_path)
                print(f'{SUCCESS}[{index}/{len(audio_files)}] COPIED: {safe_artist} -> {safe_title}')
            else:
                print(f'{INFO}[{index}/{len(audio_files)}] SKIPPED (Already exists): {safe_title}')

        except Exception as e:
            print(f'{ERROR}-' * 40)
            print(f'{ERROR}[{file_path.name}] -> CRASHED: {str(e)}')
            print(f'{ERROR}-' * 40)

    # Return the data we want to display :)
    return len(audio_files), len(processed_albums), len(processed_artists)

if __name__ == '__main__':
    # target_folder = input('Enter the path to the folder to be organised:\n')
    target_folder = 'C:\\Users\\milan\\Downloads\\Unorganised Music\\Old Files'
    target_folder = target_folder.strip('"').strip("'")
    # target_path = input('Enter the path to the folder to send the music:\n')
    target_path = 'C:\\Users\\milan\\Downloads\\Unorganised Music\\SyncedMusic'

    # Remove accidental quotations from input.
    target_path = target_path.strip('"').strip("'")

    start_time = time.perf_counter()

    total_songs, total_albums, total_artists = organise_directory(target_folder, target_path)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    print(f'\n{RESET}Music Organised')
    print(f'\nSorted {INFO}{total_artists} {RESET}Artists')
    print(f'\nSorted {INFO}{total_albums} {RESET}Albums')
    print(f'\nSorted {INFO}{total_songs} {RESET}Songs')
    print(f'\nTotal execution time: {INFO}{minutes} minutes and {seconds:.2f} seconds')