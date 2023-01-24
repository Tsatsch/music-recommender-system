import spotipy


class Spotify:
    def __init__(self, config: dict, secrets: dict) -> None:
        client_credentials_manager = spotipy.SpotifyClientCredentials(
            client_id=config["clientId"], client_secret=secrets["SPOTIFY_CLIENT_SECRET"]
        )
        self.connection = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )
