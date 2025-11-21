import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import GenreButton from './../components/genreButton/genreButton';
import MoodButton from './../components/moodButton/moodButton';
import ProfileIcon from './../components/profileIcon/profileIcon';
import SongBar from '../components/songBar/songBar.js';
import { useAuth } from './../hooks/authContext';
import { getGenreList } from './../lists/genreList';
import { getMoodList } from '../lists/moodList.js';
import './../App.css';
import { getRecommendedSongs } from '../lists/recommendedSongsList.js';

function App() {
  const [selectedMoods, setSelectedMoods] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  const [genreList, setGenreList] = useState([]);
  const [moodList, setMoodList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const [recommendedSongs, setRecommendedSongs] = useState([]);
  const [moodMap, setMoodMap] = useState({});
  const [genreMap, setGenreMap] = useState({});

  const handleLoadSongs = async () => {
    setRecommendedSongs([]);
    const songs = await getRecommendedSongs(
      selectedMoods.map((mood) => moodMap[mood]).filter(Boolean),
      selectedGenres.map((genre) => genreMap[genre]).filter(Boolean)
    );
    setRecommendedSongs(songs);
    console.log("Recommended Songs:", songs[0].image_url);
  };

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      try {
        const loadedGenres = await getGenreList();
        const loadedMoods = await getMoodList();

        const genreMapping = {};
        loadedGenres.forEach((genre) => {
          genreMapping[genre.name] = genre.id;
        });

        const moodMapping = {};
        loadedMoods.forEach((mood) => {
          moodMapping[mood.name] = mood.id;
        });

        setGenreList(loadedGenres.map((g) => g.name));
        setMoodList(loadedMoods.map((m) => m.name));
        setGenreMap(genreMapping);
        setMoodMap(moodMapping);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const toggleMood = (moodName) => {
    setSelectedMoods((prevSelected) => {
      if (prevSelected.includes(moodName)) {
        return prevSelected.filter((name) => name !== moodName);
      } else {
        return [...prevSelected, moodName];
      }
    });
  };

  const toggleGenre = (genreName) => {
    setSelectedGenres((prevSelected) => {
      if (prevSelected.includes(genreName)) {
        return prevSelected.filter((name) => name !== genreName);
      } else {
        return [...prevSelected, genreName];
      }
    });
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

      <div className='song-container'>
        <h2 className='song-header'>Songs</h2>
        {recommendedSongs.map((song, index)=> (
            <SongBar
              index = {index + 1}
              song_title={song.title}
              artist={song.artist}
              url={song.image_url}
            />
        ))}

      </div>

      <div className='selection-container'>
        <div className="genre-container">
          <h2>Genres</h2>
          {genreList.map((genre) => (
            <GenreButton
              key={genre} // Add a unique key
              genreName={genre}
              isActive={selectedGenres.includes(genre)}
              onClick={() => toggleGenre(genre)}
            />
          ))}
        </div>
        <div className="mood-container">
          <h2>Moods</h2>
          {moodList.map((mood) => (
            <MoodButton
              key={mood} // Add a unique key
              moodName={mood}
              isActive={selectedMoods.includes(mood)}
              onClick={() => toggleMood(mood)}
            />
          ))}
        </div>
      </div>

      <div className="top-songs-container">
        <button className="top-songs-button" onClick={(handleLoadSongs)}>
          Load Songs
        </button>
      </div>
    </div>
  );
}

export default App;