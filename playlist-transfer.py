from googleapiclient.discovery import build
import requests

# YouTube API configuration
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


# Fetch playlist data from JioSaavn
def fetch_jiosaavn_playlist(playlist_url):
    """
    Fetches song titles from a JioSaavn playlist URL using unofficial API.
    """
    try:
        response = requests.get(f"https://saavn.me/playlists?url={playlist_url}")
        response.raise_for_status()
        playlist_data = response.json()
        songs = [f"{song['title']} {song['primaryArtists']}" for song in playlist_data.get("songs", [])]
        return songs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JioSaavn playlist: {e}")
        return []


# Create a playlist on YouTube Music
def create_youtube_playlist(playlist_name):
    """
    Creates a new playlist on YouTube Music and returns its ID.
    """
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": playlist_name, "description": "Imported from JioSaavn", "tags": ["music", "playlist"]},
            "status": {"privacyStatus": "private"}
        }
    )
    response = request.execute()
    print(f"Created YouTube playlist: {playlist_name}")
    return response['id']


# Search and add songs to the YouTube Music playlist
def add_songs_to_youtube_playlist(playlist_id, song_titles):
    """
    Searches for each song on YouTube Music and adds it to the specified playlist.
    Tracks and displays songs that couldn't be found.
    """
    not_found_songs = []  # List to store songs not found

    for song in song_titles:
        try:
            # Search for the song on YouTube
            search_response = youtube.search().list(
                part="snippet",
                q=song,
                type="video",
                maxResults=1
            ).execute()

            if not search_response['items']:
                print(f"Song not found on YouTube: {song}")
                not_found_songs.append(song)
                continue

            # Extract video ID and add to the playlist
            video_id = search_response['items'][0]['id']['videoId']
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id}
                    }
                }
            ).execute()
            print(f"Added song to playlist: {song}")
        except Exception as e:
            print(f"Error adding song to playlist: {song} | Error: {e}")
            not_found_songs.append(song)

    return not_found_songs


# Main function for multiple playlists
if __name__ == "__main__":
    # List of JioSaavn playlist URLs
    JIOSAAVN_PLAYLISTS = [
        {"name": "My Favorite Playlist", "url": "YOUR_JIOSAAVN_PLAYLIST_URL_1"},
        {"name": "Chill Vibes", "url": "YOUR_JIOSAAVN_PLAYLIST_URL_2"},
        {"name": "Workout Hits", "url": "YOUR_JIOSAAVN_PLAYLIST_URL_3"}
    ]

    # Process each playlist
    for playlist in JIOSAAVN_PLAYLISTS:
        playlist_name = playlist["name"]
        playlist_url = playlist["url"]

        print(f"\nProcessing playlist: {playlist_name}")

        # Step 1: Fetch songs from JioSaavn
        songs = fetch_jiosaavn_playlist(playlist_url)
        if not songs:
            print(f"No songs found in the JioSaavn playlist: {playlist_name}")
            continue

        print(f"Fetched {len(songs)} songs from JioSaavn playlist: {playlist_name}")

        # Step 2: Create a new playlist on YouTube Music
        youtube_playlist_id = create_youtube_playlist(playlist_name)

        # Step 3: Add songs to the YouTube Music playlist
        not_found_songs = add_songs_to_youtube_playlist(youtube_playlist_id, songs)

        # Display summary for the current playlist
        print(f"\nSummary for {playlist_name}:")
        print(f"  Total Songs Processed: {len(songs)}")
        print(f"  Songs Added Successfully: {len(songs) - len(not_found_songs)}")
        print(f"  Songs Not Found: {len(not_found_songs)}")

        if not_found_songs:
            print(f"  Unfound Songs: {not_found_songs}")

    print("\nAll playlists processed!")
