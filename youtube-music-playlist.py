
import os, requests
from googleapiclient.discovery import build

# Define the YouTube Data API key and service
YOUTUBE_API_KEY = ''
#YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def get_youtube_song_details(songs):
    song_details_list = []
    not_found_songs = []  # List to store songs that couldn't be found

    for song in songs:
        song_name = song.get('name', 'Unknown Song')
        print(song.get('year', 'Unknown year'))
        song_year = song.get('year', 'Unknown year')

        # Search for the song on YouTube
        search_response = youtube.search().list(
            q=song_name,
            part='id,snippet',
            maxResults=1
        ).execute()

        print(search_response)

        # Check if results were returned
        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            video_title = search_response['items'][0]['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_duration = "Unknown Duration"  # YouTube API does not provide duration in search
            video_release_date = search_response['items'][0]['snippet'].get('publishedAt', 'Unknown Release Date')

            song_details = {
                'name': video_title,
                'id': video_id,
                'url': video_url,
                'releaseDate': video_release_date,
                'duration': video_duration,
                'language': song.get('language', 'Unknown Language'),
                'explicitContent': song.get('explicitContent', False)
            }

            song_details_list.append(song_details)
        else:
            # If no result found, add the song to the not_found_songs list
            not_found_songs.append(song_name)

    # Display songs that were not found on YouTube
    if not_found_songs:
        print("Songs not found on YouTube:")
        for song in not_found_songs:
            print(f"- {song}")

    return song_details_list



def fetch_jiosaavn_playlist():
    """
    Fetches playlist details from JioSaavn and returns a list of songs with their details.
    """
    try:
        # API endpoint for fetching JioSaavn playlist
        response = requests.get(
            "https://saavn.dev/api/playlists?link=https://www.jiosaavn.com/s/playlist/758b524bfdd726ff19add70aa03d0ccb/anime-%f0%9f%92%a2/EHBorBKoxU7Exeh5N5JWFg__&limit=1000")
        response.raise_for_status()

        # Parse response JSON
        playlist_data = response.json()

        songs = playlist_data['data'].get('songs', [])
        playlist_name = playlist_data.get('data', {}).get('name', 'Unknown Playlist')
        print(f"\nPlaylist: {playlist_name}")
        print(f"Total Songs: {len(songs)}\n")

        song_list = []

        # Iterate through each song in the playlist
        for song in songs:
            song_details = {
                'name': song.get('name', 'Unknown Song'),
                'id': song.get('id', 'Unknown ID'),
                'url': song.get('url', 'No URL'),
                'releaseDate': song.get('releaseDate', 'Unknown Release Date'),
                'duration': song.get('duration', 'Unknown Duration'),
                'language': song.get('language', 'Unknown Language'),
                'explicitContent': song.get('explicitContent', False)
            }

            song_list.append(song_details)

        return song_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching playlist: {e}")
        return []




if __name__ == "__main__":
    # Example playlist URL

    # Example input: array of songs with given attributes
    songs = fetch_jiosaavn_playlist()

    # Fetch song details from YouTube
    song_details = get_youtube_song_details(songs)

    # Print the details of each song
    for song in song_details:
        print(f"Song: {song['name']}")
        print(f"ID: {song['id']}")
        print(f"URL: {song['url']}")
        print(f"Release Date: {song['releaseDate']}")
        print(f"Duration: {song['duration']}")
        print(f"Language: {song['language']}")
        print(f"Explicit Content: {song['explicitContent']}")
        print('-' * 40)
