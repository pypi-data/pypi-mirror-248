### How to use the Package

Run `pip install connect_spotify`

```
from connect_spotify import ConnectionAPI
conn = ApiConnection(
    token=SPOTIFY_API_TOKEN
)
conn._connect()
conn.get_artist_name('the strokes')
#returns artist data
```

### Description

[Original Repo](https://github.com/Satoshi-Sh/streamlit-api)
This application was created to join Streamlit Hackathon. It data visualizes music artist popularities by bar and line plots. Streamlit connection was used to interact with Spotify API.

### How to Run

- Run `pip intall`
- Create secrets.toml according to the sample.secrets.toml. You need to get your client secret from Spotify
- Run `streamlit run app.py`

### Live page

[Live Page](https://spotify-dataviz.streamlit.app/)

Streamlit kindly provides the community cloud server for streamlit app.
Follow the instructions of the [link](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app) if you want to deploy it on your own.

<p align="center">
  <img alt="musicians popularity plots." src="https://res.cloudinary.com/dmaijlcxd/image/upload/v1703729138/connection-thumbnail_tvztoh.png">
</p>
