from pathlib import Path
import time, shutil
from helpers import FormatText, get_song_metadata, get_artist_img, copy_album_img

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

            if new_folder not in processed_albums:
                file_parent_folder = file_path.parent
                album_art_status = copy_album_img(file_parent_folder, new_folder, supported_image_extensions)

                match album_art_status:
                    case 'MISSING':
                        print(FormatText.alert(f'NO ALBUM ART IN FOLDER {FormatText.info(file_parent_folder)}'))
                    case 'EXISTS':
                        print(FormatText.info(f'ALBUM ART: {metadata.album} ALREADY EXISTS'))
                    case 'COPIED':
                        print(FormatText.success(f'COPIED ALBUM ART: {FormatText.info(metadata.album)}'))
                    case _:
                        print(FormatText.error('An Error occurred'))
                processed_albums.add(new_folder)

            get_artist_img()
            
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
                        print(FormatText.success(f'COPIED ARTIST PICTURE: {metadata.album_artist}'))

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

if __name__ == '__main__':
    original_folder = input(FormatText.alert('\nEnter the path to the folder to be organised:\n'))
    destination_folder = input(FormatText.alert('\nEnter the path to the folder to send the music:\n'))

    # Remove accidental quotations from input.
    original_folder = original_folder.strip('"').strip("'")
    destination_folder = destination_folder.strip('"').strip("'")

    start_time = time.perf_counter()

    total_songs, total_albums, total_artists = organise_directory(original_folder, destination_folder)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    print(FormatText.alert('\nMusic Organised'))
    print(f'\nSorted {FormatText.info(total_artists)} Artists')
    print(f'\nSorted {FormatText.info(total_albums)} Albums')
    print(f'\nSorted {FormatText.info(total_songs)} Songs')
    print(f'\nTotal execution time: {FormatText.info(f'{minutes} minutes and {seconds:.2f} seconds')}')