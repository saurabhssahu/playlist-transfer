import requests


def fetch_jiosaavn_playlist():
    """
    Fetches playlist details from JioSaavn and returns a list of songs with their details.
    """
    try:
        # API endpoint for fetching JioSaavn playlist
        response = requests.get("https://saavn.dev/api/playlists?link=https://www.jiosaavn.com/s/playlist/758b524bfdd726ff19add70aa03d0ccb/a-%f0%9f%98%8c%f0%9f%92%94/MPGMoRo1EVwGSw2I1RxdhQ__&limit=1000")
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
    #playlist_url = input("Enter the JioSaavn playlist URL: ").strip()
    print(fetch_jiosaavn_playlist())
