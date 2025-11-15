import React, { useState, useEffect } from 'react'
import GenreButton from './../components/genreButton/genreButton'
import MoodButton from './../components/moodButton/moodButton'
import './../App.css'

function App() {
  const [username, setUsername] = useState("John Doe");
  const [selectedMoods, setSelectedMoods] = useState([]);
  // const [moodList, setMoodList] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  // const [genreList, setGenreList] = useState([]);

  const genreList = ['EDM', 'Pop', 'KPOP'];

  const toggleMood = (moodName) => {
    setSelectedMoods(prevSelected => {
      if(prevSelected.includes(moodName)) {
        return prevSelected.filter(name => name !== moodName);
      }
      else{
        return [...prevSelected, moodName];
      }
    })
  };

  const toggleGenre = (genreName) => {
    setSelectedGenres(prevSelected => {
      if(prevSelected.includes(genreName)) {
        return prevSelected.filter(name => name !== genreName);
      }
      else{
        return [...prevSelected, genreName];
      }
    })
  };

  return (
    <div>
      <h1 className="title">Hello {username}</h1>
      <div className='selection-container'>
        <div className="genre-container">
          <h2>Genres</h2>
          {genreList.map(genreName => (
            <GenreButton
              genreName={genreName}
              isActive={selectedGenres.includes({genreName})}
              onClick={() => toggleGenre({genreName})}
            />
          ))}
        </div>
        <div className="mood-container">
          <h2>Moods</h2>
          <MoodButton 
            moodName="happy"
            isActive = {selectedMoods.includes('happy')}
            onClick={() => toggleMood('happy')}
          />
        </div>
      </div>
      <div className="top-songs-container">
        <button className="top-songs-button">Top 50 Hits</button>
      </div>
    </div>
  )
}

export default App