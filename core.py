import shutil
from pathlib import Path
from helpers import FormatText, get_song_metadata, copy_artist_img, copy_album_img

def organise_directory(source_path: str, target_path: str):
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

    # Set to store the PATH of albums we've found
    processed_albums = set()
    # Set to store the PATH of the artists we've found.
    processed_artists = set()

    print(f'Found {FormatText.info(len(audio_files))} audio files. Reading Metadata...\n')
    print('-' * 40)

    for index, file_path in enumerate(audio_files, 1):
        try:
            metadata = get_song_metadata(file_path)

            if metadata is None:
                continue

            artist_folder = target_dir / metadata.album_artist
            new_folder = target_dir / metadata.album_artist / metadata.album
            new_folder.mkdir(parents=True, exist_ok=True)

            new_file_path = new_folder / f'{metadata.title}{file_path.suffix.lower()}'

            # Copy Album Art
            if new_folder not in processed_albums:
                album_art_status = copy_album_img(file_path.parent, new_folder, allowed_extensions=supported_image_extensions)

                match album_art_status:
                    case 'MISSING':
                        print(FormatText.alert(f'NO ALBUM ART IN FOLDER {FormatText.info(file_path.parent)}'))
                    case 'EXISTS':
                        print(FormatText.info(f'ALBUM ART: {metadata.album} ALREADY EXISTS'))
                    case 'COPIED':
                        print(FormatText.success(f'COPIED ALBUM ART: {FormatText.info(metadata.album)}'))
                    case _:
                        print(FormatText.error('An Error occurred'))
                processed_albums.add(new_folder)

            # Copy Artist Art
            if artist_folder not in processed_artists:
                artist_art_status = copy_artist_img(file_path.parent, artist_folder, allowed_extensions=supported_image_extensions)

                match artist_art_status:
                    case 'MISSING':
                        print(FormatText.alert(f'NO ARTIST ART IN FOLDER {FormatText.info(artist_folder)}'))
                    case 'EXISTS':
                        print(FormatText.info(f'ARTIST ART FOR: {metadata.artist} ALREADY EXISTS'))
                    case 'COPIED':
                        print(FormatText.success(f'COPIED ARTIST PICTURE: {metadata.album_artist}'))
                    case _:
                        print(FormatText.error('An Error occurred'))

                processed_artists.add(artist_folder)

            if not new_file_path.exists():
                shutil.copy2(file_path, new_file_path)
                print(FormatText.success(f'[{index}/{len(audio_files)}] COPIED: {metadata.artist} -> {metadata.album} -> {metadata.title}'))
            else:
                print(FormatText.info(f'[{index}/{len(audio_files)}] SKIPPED (Already exists): {metadata.title}'))

        except Exception as e:
            print(FormatText.error(f'[{file_path.name}] -> CRASHED: {str(e)}'))

    # Return the data we want to display :)
    return len(audio_files), len(processed_albums), len(processed_artists)