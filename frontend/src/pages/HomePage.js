import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import GenreButton from './../components/genreButton/genreButton'
import MoodButton from './../components/moodButton/moodButton'
import ProfileIcon from './../components/profileIcon/profileIcon'
import { useAuth } from './../hooks/authContext'
import { getGenreList } from './../lists/genreList'
import { getMoodList } from '../lists/moodList.js'
import './../App.css'

function App() {
  const [selectedMoods, setSelectedMoods] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  const [genreList, setGenreList] = useState([]);
  const [moodList, setMoodList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      try {
        const loadedGenres = await getGenreList();
        const loadedMoods = await getMoodList();
        setGenreList(loadedGenres);
        setMoodList(loadedMoods);
      } catch (error) {
        console.error("Failed to load data:", error)
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

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

      <div className='header'>
        <div>
          <h1 className="title">Hello, {user.username}</h1>
        </div>
        <div 
          className='header-icon-container'
          onClick={() => navigate('/profile')}
        >
          <ProfileIcon/>
        </div>
      </div>

      <div className='selection-container'>
        <div className="genre-container">
          <h2>Genres</h2>
          {genreList.map((genre) => (
              <GenreButton
                genreName={genre}
                isActive={selectedGenres.includes(genre)}
                onClick={()=>toggleGenre(genre)}
              />
            ))}
        </div>
        <div className="mood-container">
          <h2>Moods</h2>
          {moodList.map((mood) => (
              <MoodButton
                moodName={mood}
                isActive={selectedMoods.includes(mood)}
                onClick={()=>toggleMood(mood)}
              />
            ))}
        </div>
      </div>

      <div className="top-songs-container">
        <button className="top-songs-button">Load Songs</button>
      </div>
    </div>
  )
}

export default App