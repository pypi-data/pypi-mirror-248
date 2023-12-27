import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os
import logging

def main():
    print("Console is not supported.")

class ngdl:
    @staticmethod
    def get_data(id: int):
        url = f'https://www.newgrounds.com/audio/listen/{id}'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка наличия ошибок при запросе
            if response.status_code != 200: 
                print("Error: Failed to retrieve song information.")
                logging.error("Error: Failed to retrieve song information.")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Ищем элементы на странице для получения информации
            title_element = soup.find('h2', class_='rated-e')
            author_container = soup.find('h4', class_='smaller')
            artist = author_container.find('a').text.strip() if author_container else 'N/A'
            rating_element = soup.find('span', class_='pod-head-rating')

            # Idiotism
            dd_genre_container = soup.find('dl', class_="sidestats flex-1")
            genre_container = dd_genre_container.find('dd') if dd_genre_container else 'N/A'
            genre_element = genre_container.find('a').text.strip() if genre_container else 'N/A'
            
            title = title_element.text.strip() if title_element else 'N/A'
            genre = genre_element if genre_element else 'N/A'
            rating = rating_element.text.strip() if rating_element else 'E'

            song_info = {
                'title': title,
                'artist': artist,
                'genre': genre,
                'rating': rating,
            }

            return song_info
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None

    @staticmethod
    def download_music(id: int, output_folder="./"):
        song_info = ngdl.get_data(id=id)
        if song_info is None:
            print("Failed to retrieve song information.")
            logging.error("Failed to retrieve song information.")
            return

        song_name_old = song_info['title']
        song_name = song_name_old.replace(" ", "-")

        # Формирование URL для скачивания
        base_url = 'https://audio.ngfiles.com'
        folder_id = str(id)[:4] + '000'
        audio_url = f'{base_url}/{folder_id}/{id}_{song_name}.mp3'

        try:
            # Загрузка музыки
            audio_data = requests.get(audio_url).content
            output_path = os.path.join(output_folder, f"{id}_{song_name}.mp3")

            with open(output_path, 'wb') as audio_file:
                audio_file.write(audio_data)

            print(f"Music downloaded: {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")

    @staticmethod
    async def get_data_async(id: int):
        url = f'https://www.newgrounds.com/audio/listen/{id}'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # Проверка наличия ошибок при запросе
                    if response.status != 200:
                        print("Error: Failed to retrieve song information.")
                        logging.error("Error: Failed to retrieve song information.")
                        return None

                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    # Ищем элементы на странице для получения информации
                    title_element = soup.find('h2', class_='rated-e')
                    author_container = soup.find('h4', class_='smaller')
                    artist = author_container.find('a').text.strip() if author_container else 'N/A'
                    rating_element = soup.find('span', class_='pod-head-rating')
        
                    # Idiotism
                    dd_genre_container = soup.find('dl', class_="sidestats flex-1")
                    genre_container = dd_genre_container.find('dd') if dd_genre_container else 'N/A'
                    genre_element = genre_container.find('a').text.strip() if genre_container else 'N/A'
                    
                    title = title_element.text.strip() if title_element else 'N/A'
                    genre = genre_element if genre_element else 'N/A'
                    rating = rating_element.text.strip() if rating_element else 'E'
        
                    song_info = {
                        'title': title,
                        'artist': artist,
                        'genre': genre,
                        'rating': rating,
                    }
        
                    return song_info

        except Exception as e:
            print(f"Error during request: {e}")
            return None

    @staticmethod
    async def download_music_async(id: int, output_folder="./"):
        song_info = await ngdl.get_data_async(id=id)
        if song_info is None:
            print("Failed to retrieve song information.")
            logging.error("Failed to retrieve song information.")
            return

        song_name_old = song_info['title']
        song_name = song_name_old.replace(" ", "-")

        # Формирование URL для скачивания
        base_url = 'https://audio.ngfiles.com'
        folder_id = str(id)[:4] + '000'
        audio_url = f'{base_url}/{folder_id}/{id}_{song_name}.mp3'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as audio_response:
                    audio_response.raise_for_status()

                    # Загрузка музыки
                    audio_data = await audio_response.read()
                    output_path = os.path.join(output_folder, f"{id}_{song_name}.mp3")

                    with open(output_path, 'wb') as audio_file:
                        audio_file.write(audio_data)

                    print(f"Music downloaded: {output_path}")
        except aiohttp.ClientResponseError as e:
            print(f"Error during request: {e}")

if __name__ == "__main__":
    main()

# Замените SONG_ID на реальный идентификатор песни
# song_id = 1154735
# audio_url = download_music(song_id)

# if audio_url:
#     print(f"Audio URL: {audio_url}")

#     # Загрузка музыки
#     audio_data = requests.get(audio_url).content
#     with open("downloaded_music.mp3", 'wb') as audio_file:
#         audio_file.write(audio_data)
#     print("Music downloaded.")
# else:
#     print("Failed to retrieve audio information.")
