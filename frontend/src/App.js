import React, { useState } from 'react';

function App() {
  const [songName, setSongName] = useState('');
  const [artistName, setArtistName] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [sentiment, setSentiment] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('https://spotify-copy-project-be8z.vercel.app', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ song_name: songName, artist_name: artistName }),
    });

    const data = await response.json();
    setSentiment(data.sentiment);
    setRecommendations(data.recommendations);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-8">
      <h1 className="text-4xl font-bold mb-8 text-center">🎵 Modern Song Recommendation System 🎶</h1>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center bg-gray-800 p-6 rounded-lg shadow-lg space-y-4 w-full max-w-md"
      >
        <input
          type="text"
          placeholder="Enter Song Name"
          value={songName}
          onChange={(e) => setSongName(e.target.value)}
          className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          placeholder="Enter Artist Name"
          value={artistName}
          onChange={(e) => setArtistName(e.target.value)}
          className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg"
        >
          Get Recommendations
        </button>
      </form>

      {sentiment && (
        <div className="mt-12 w-full max-w-5xl">
          <h2 className="text-2xl font-semibold mb-6">Sentiment: <span className="text-blue-400">{sentiment}</span></h2>
          <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className="bg-gray-800 p-4 rounded-lg shadow-lg transform transition duration-300 hover:scale-105"
              >
                <img
                  src={rec.album_cover}
                  alt={`${rec.track_name} cover`}
                  className="w-full h-48 object-cover rounded-lg mb-4"
                />
                <p className="text-lg font-bold truncate">{rec.track_name}</p>
                <p className="text-sm text-gray-400">{rec.artist_name}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

