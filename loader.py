import requests as req
import sys
from getpass import getuser
import os
from time import time

try:
    import colorama
    from colorama import Fore, Style
except ImportError:
    print(f'Colorama not found.... Installing!')
    os.system('pip install colorama')
    import colorama
    from colorama import Fore, Style

    os.system('cls' if os.name == 'nt' else 'clear')

BRIGHT = Style.BRIGHT
BASE_FOLDER = f'C:/Users/{getuser()}/Music/Loader/'
API = 'dfcb6d76f2f6a9894gjkege8a44563255'

try:
    from rich.progress import track
except ImportError:
    print(f'{BRIGHT}{Fore.RED}Rich not found.... Installing!')
    print(f'{Fore.YELLOW}')
    os.system('pip install rich')
    from rich.progress import track

    os.system('cls' if os.name == 'nt' else 'clear')


def check_connectivity():
    r1 = req.get(f'https://loader.to/ajax/api.php?api={API}&q=&function=s')
    # print(r1)
    try:
        if r1.json():
            print(f'{BRIGHT}{Fore.GREEN}Working')
        else:
            print(f'{BRIGHT}{Fore.RED}Network Error')
            sys.exit(0)
    except Exception as e:
        print(f'{BRIGHT}{Fore.RED}{str(e)}')
        print(f'{BRIGHT}{Fore.RED}Existing..!')
        sys.exit(0)


def search_and_results():
    os.system('cls' if os.name == 'nt' else 'clear')
    url = input(f'{BRIGHT}{Fore.CYAN}Enter YT video url or name -> ')

    r2 = req.get(f'https://loader.to/ajax/api.php?api={API}&q={url.replace(" ", "+")}&function=s')

    results = []
    for each in r2.json()['items']:
        # try:
        try:
            title = each['title']
        except:
            continue
        try:
            yt_link = each['url']
        except:
            continue
        duration = each.get('duration')
        try:
            author = each['author']['name']
        except:
            author = 'None'
        try:
            views = each['views']
        except:
            views = 0

        results.append([title, yt_link, duration, author, views])

    results.sort(key=lambda x: x[4])

    for index, each in enumerate(results):
        print()
        print(f'{BRIGHT}{Fore.RED}{index}.', end='')
        print(f'{BRIGHT}{Fore.YELLOW}{each[0]}\n{each[3]} - {each[2]} - {each[-1]}')

    print()
    selected_results = []
    print(f'''
{BRIGHT}{Fore.CYAN}Examples:
    1       -> Single selection
    1,3,4   -> Multiple selection
    1-4     -> Range selection (reverse applicable)
    1,2,3-5 -> Advanced selection
    (empty) -> Search again''')

    while True:
        try:
            selected = input(f'{BRIGHT}{Fore.GREEN}Download -> ')
            if selected.strip() == '':
                return search_and_results()

            parts = selected.split(',')
            for part in parts:
                if '-' in part:
                    first = int(part.split('-')[0])
                    end = int(part.split('-')[1])
                    if first > end:
                        temp = first
                        first = end
                        end = temp

                    for i in range(first, end + 1):
                        song_name = name_correction(results[i][0])
                        song_url = results[i][0]
                        selected_results.append([song_name, song_url])

                else:
                    selected_results.append([results[int(part)][0], results[int(part)][1]])
            break
        except Exception as exception:
            print(f'{Style.BRIGHT}{Fore.RED}{str(exception)}')
            continue
    return selected_results


def name_correction(song_name):
    illegal = "#%&{}\\<>*?/$!'\":@+`|=\n\t()"
    alphabet = 'asdfghjklqwertyuiopzxcvbnm QWERTYUIOPLKJHGFDSAZXCVBNM'
    for each in illegal:
        song_name = song_name.replace(each, '')
    build = ''
    for each in song_name:
        if each in alphabet:
            build += each
    song_name = build
    return '_'.join([word for word in song_name.split()])


def select_download_option():
    os.system('cls' if os.name == 'nt' else 'clear')

    download_option = [
        [' Audio MP3', 'mp3', 'mp3'],
        [' Audio M4A', 'm4a', 'm4a'],
        [' Audio WEBM', 'webm', 'webm'],
        [' Audio AAC', 'aac', 'm4a'],
        [' Audio FLAC', 'flac', 'flac'],
        [' Audio OPUS', 'opus', 'opus'],
        [' Audio OGG', 'ogg', 'ogg'],
        [' Audio WAV', 'wav', 'wav'],
        [' Video MP4(360p)', '360', 'mp4'],
        [' Video MP4(480p)', '480', 'mp4'],
        ['Video MP4(720p)', '720', 'mp4'],
        ['Video MP4(1080p)', '1080', 'mp4'],
        ['Video MP4(1440p)', '1440', 'mp4'],
        ['Video WEBM(4K)', '4k', 'webm'],
        ['Video WEBM(8K)', '8k', 'webm'],
    ]

    extension = 'm4a'
    file_type = 'm4a'

    for index, each in enumerate(download_option):
        print(f'\t{BRIGHT}{Fore.RED}{str(index)}', end=' ')
        print(f'{BRIGHT}{Fore.LIGHTGREEN_EX}{each[0]}')

    print()
    while True:
        try:
            option = input(f'{BRIGHT}{Fore.GREEN}Download Option -> ')
            if option.strip() == '':
                break
            extension = download_option[int(option)][1]
            file_type = download_option[int(option)][2]
            break
        except ValueError:
            continue
        except IndexError:
            continue
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{str(e)}')
            sys.exit(0)

    return extension, file_type


def downloader(results, extension, file_type):
    song_for_playing = ''
    for song_number, each in enumerate(results, start=1):
        print()
        print(f'{Style.BRIGHT}{Fore.MAGENTA}({song_number}/{len(results)}) {each[0]}')
        r3 = req.get(f'https://loader.to/ajax/download.php?api={API}&format={extension}&url={each[1]}')

        task_id = r3.json()['id']
        print(f'\t{BRIGHT}{Fore.LIGHTBLUE_EX}Task ID - {task_id}')

        text = None
        progress = None
        while True:
            r4 = req.get(
                f'https://loader.to/ajax/progress.php?api=dfcb6d76f2f6a9894gjkege8a44563255&id={r3.json()["id"]}')
            if r4.json()['success'] == 1:
                break
            if text is None and progress is None:
                text = r4.json()['text']
                progress = r4.json()['progress']
                continue

            elif text == r4.json()['text'] and progress == r4.json()['progress']:
                continue
            else:
                text = r4.json()['text']
                progress = r4.json()['progress']
            print(f"\t{BRIGHT}{Fore.YELLOW}{r4.json()['text']} {r4.json()['progress']} %")

        download_url = r4.json()['download_url']
        print(f'\t{BRIGHT}{Fore.GREEN}Download Link - ', download_url)

        r5 = req.get(download_url, stream=True)

        song_name = each[0] + '.' + file_type
        song_name = name_correction(song_name)
        song_for_playing = song_name
        chunk_size = 1024
        try:
            total = round(int(r5.headers['Content-Length']) / chunk_size)
            size_ = str(round(total / 1024, 2))
            print(song_name)
            with open(f'{song_name}', 'wb') as f:
                for data in track(r5.iter_content(chunk_size=chunk_size),
                                  description=f'{Style.BRIGHT}{Fore.RED}Downloading {str(size_)}MB', transient=False,
                                  total=total):
                    f.write(data)
        except KeyError:
            with open(f'{song_name}', 'wb') as f:
                for data in track(r5.iter_content(chunk_size=chunk_size), description='Downloading', transient=False):
                    f.write(data)

    # 18
    # os.system(f'start .\\"{song_for_playing}"')
    os.system(f'.\\"{song_for_playing}"')
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    if not os.path.isdir(BASE_FOLDER):
        os.mkdir(BASE_FOLDER)

    os.chdir(BASE_FOLDER)
    os.system('cls' if os.name == 'nt' else 'clear')

    x = os.getcwd()
    check_connectivity()
    results = search_and_results()

    
    extension, file_type = select_download_option()
    started = time()
    downloader(results, extension, file_type)
    ended = time()

    elapsed = round(ended - started, 2)
    print(f'{Style.BRIGHT}{Fore.GREEN}{str(len(results))} downloaded in {str(elapsed)} seconds!')


if __name__ == '__main__':
    main()
