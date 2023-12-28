import streamlit as st
from streamlit.connections import BaseConnection
import requests


class ApiConnection(BaseConnection):
    def __init__(self, token):
        self.token = token

    def _connect(self) -> requests.Session:
        session = requests.Session()
        session.headers['Authorization'] = 'Bearer ' + self.token
        return session

    def get_spotify_artist(self, artist_name):
        # API endpoint for searching artists
        search_url = "https://api.spotify.com/v1/search"

        # Set up the search parameters
        params = {
            "q": artist_name,
            "type": "artist"
        }

        # Make the API call using the 'requests' library
        response = self._connect().get(search_url, params=params)

        # Check if the API call was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON to extract the artist ID
            response_data = response.json()
            artists = response_data.get("artists", {}).get("items", [])
            if artists:
                # Return the first artist's ID (you may want to handle multiple results differently)
                return artists[0]
        else:
            # Handle error scenarios here
            return None
