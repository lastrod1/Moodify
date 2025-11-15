import "./genreButton.css"

function genreButton({ genreName, isActive, onClick }) {
  return (
    <button onClick={onClick} className={`genre-button ${isActive ? 'active' : ''}`}>
      {genreName}
    </button>
  )
}

export default genreButton