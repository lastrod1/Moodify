import React, { useState, useEffect } from 'react'
import GenreButton from './components/genreButton/genreButton'
import MoodButton from './components/moodButton/moodButton'
import './App.css'

function App() {
  const [username, setUsername] = useState("John Doe");
  return (
    <div>
      <h1 class="title">Hello {username}</h1>
      <div class="genre-container">
        <h2>Genres</h2>
        <GenreButton genreName="EDM"/>
      </div>
      <div class="mood-container">
        <h2>Moods</h2>
        <MoodButton moodName="happy"/>
      </div>
      <div class="top-songs-container">
        <button class="top-songs-button">Top 50 Hits</button>
      </div>
    </div>
  )
}

export default App