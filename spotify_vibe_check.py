import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with Windows environment variable
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

def get_playlist_name(mood):
    """Generate a short, creative playlist name based on the mood."""
    prompt = f"""Based on this mood/vibe: {mood}, generate a short, creative playlist name (maximum 2 words).
    The name should be catchy and reflect the mood. Return only the name, nothing else."""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative music expert that generates short, catchy playlist names."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def get_ai_recommendations(artists, mood):
    """Get song recommendations from OpenAI based on artists and mood."""
    # Extract any "not like" or "nothing like" mentions from the mood
    unwanted_artists = []
    if "not like" in mood.lower() or "nothing like" in mood.lower():
        # Simple parsing - you might want to improve this
        parts = mood.lower().split("not like" if "not like" in mood.lower() else "nothing like")
        if len(parts) > 1:
            unwanted_artists = [artist.strip() for artist in parts[1].split(",")]
            # Clean up the mood text
            mood = parts[0].strip()
    
    prompt = f"""Based on these artists: {', '.join(artists)} and the mood/vibe: {mood},
    suggest 20 songs that would complement this vibe. 
    
    IMPORTANT RULES:
    1. DO NOT include any songs by these artists: {', '.join(unwanted_artists) if unwanted_artists else 'none'}
    2. Focus on the exact style and era mentioned in the mood
    3. Format the response as a simple list of song names, one per line
    4. Do not include any additional text or formatting"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a music expert that suggests songs based on artists and mood. You must strictly follow the user's preferences and exclusions."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Split the response into a list of songs
    songs = response.choices[0].message.content.strip().split('\n')
    return songs

def get_available_devices(sp):
    """Get list of available Spotify devices."""
    devices = sp.devices()
    return devices['devices']

def create_spotify_playlist(artists, mood):
    """Create a Spotify playlist with recommended songs."""
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope='playlist-modify-public user-modify-playback-state'
    ))
    
    # Get AI recommendations
    recommended_songs = get_ai_recommendations(artists, mood)
    
    # Search for each song on Spotify and collect URIs
    track_uris = []
    for song in recommended_songs:
        try:
            result = sp.search(q=song, type='track', limit=1)
            if result['tracks']['items']:
                track_uris.append(result['tracks']['items'][0]['uri'])
        except Exception as e:
            print(f"Error searching for song {song}: {e}")
    
    if not track_uris:
        print("No songs found to add to the playlist.")
        return
    
    # Generate playlist name
    playlist_name = get_playlist_name(mood)
    
    # Create a new playlist
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    
    # Add tracks to the playlist
    sp.playlist_add_items(playlist['id'], track_uris)
    
    print(f"\nCreated playlist: {playlist_name}")
    print(f"Playlist URL: {playlist['external_urls']['spotify']}")
    
    # Try to start playback
    try:
        # Get available devices
        devices = get_available_devices(sp)
        
        if not devices:
            print("\nNo active Spotify devices found. Please open Spotify on your computer or phone.")
            return
        
        # Try to start playback on the first available device
        device_id = devices[0]['id']
        sp.start_playback(device_id=device_id, context_uri=playlist['uri'])
        print(f"\nStarted playing on device: {devices[0]['name']}")
    except Exception as e:
        print("\nCouldn't start playback automatically. Please open the playlist URL to listen to your music.")

def main():
    print("Welcome to Spotify Vibe Check!")
    print("Enter your favorite artists (comma-separated):")
    artists_input = input().strip()
    artists = [artist.strip() for artist in artists_input.split(',')]
    
    print("\nDescribe your current mood/vibe:")
    mood = input().strip()
    
    create_spotify_playlist(artists, mood)

if __name__ == "__main__":
    main() 