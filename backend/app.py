from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Spotify setup
client_id = '64d63a5e8dc94fe7aded2c8175e64a0e'
client_secret = '3277c839fb2345ff8707929e85452821'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Sentiment analysis pipeline
sentiment_pipeline = pipeline('sentiment-analysis')

@app.route('/')
def home():
    return "Welcome to the Enhanced Song Recommendation System!"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    song_name = data.get('song_name')
    artist_name = data.get('artist_name')

    if not song_name:
        return jsonify({'error': 'Song name is required'}), 400

    # Analyze sentiment using the sentiment pipeline
    sentiment_result = sentiment_pipeline(f"{song_name} by {artist_name}")[0]
    sentiment_label = classify_sentiment(sentiment_result['score'], sentiment_result['label'])

    # Fetch recommendations from Spotify based on sentiment
    recommendations = fetch_spotify_recommendations(artist_name, sentiment_label)

    return jsonify({
        'sentiment': sentiment_label,
        'recommendations': recommendations
    })

def classify_sentiment(score, label):
    if label == "POSITIVE":
        if score >= 0.9:
            return "Very Positive"
        elif score >= 0.7:
            return "Positive"
        else:
            return "Slightly Positive"
    elif label == "NEGATIVE":
        if score >= 0.9:
            return "Very Negative"
        elif score >= 0.7:
            return "Negative"
        else:
            return "Slightly Negative"
    else:
        return "Neutral"

def fetch_spotify_recommendations(artist_name, sentiment):
    recommendations = []

    # Fetch up to 5 songs from the same artist and randomly sample 2
    same_artist_results = sp.search(q=f'artist:{artist_name}', type='track', limit=5)
    same_artist_tracks = same_artist_results['tracks']['items']
    sampled_same_artist_tracks = random.sample(same_artist_tracks, min(2, len(same_artist_tracks)))

    for track in sampled_same_artist_tracks:
        track_name = track['name']
        artist = track['artists'][0]['name']
        album_cover = track['album']['images'][0]['url']  # Get album cover
        recommendations.append({
            'track_name': track_name,
            'artist_name': artist,
            'album_cover': album_cover
        })

    # Dynamic Spotify query based on sentiment
    if "Positive" in sentiment:
        query = 'genre:pop happy'
    elif "Negative" in sentiment:
        query = 'genre:pop sad'
    elif sentiment == "Neutral":
        query = 'genre:pop chill'
    else:
        query = 'genre:pop'

    # Fetch up to 10 additional songs and randomly sample 3
    other_artists_results = sp.search(q=query, type='track', limit=10)
    other_artists_tracks = other_artists_results['tracks']['items']
    sampled_other_artist_tracks = random.sample(other_artists_tracks, min(3, len(other_artists_tracks)))

    for track in sampled_other_artist_tracks:
        track_name = track['name']
        artist = track['artists'][0]['name']
        album_cover = track['album']['images'][0]['url']  # Get album cover
        if artist.lower() != artist_name.lower():
            recommendations.append({
                'track_name': track_name,
                'artist_name': artist,
                'album_cover': album_cover
            })

    return recommendations

if __name__ == '__main__':
    app.run(debug=False)
