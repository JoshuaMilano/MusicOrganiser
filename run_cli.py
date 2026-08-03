import time
from core import organise_directory
from helpers import FormatText

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