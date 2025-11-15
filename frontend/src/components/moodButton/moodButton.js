import "./moodButton.css"

function genreButton({ moodName, isActive, onClick}) {
  return (
    <button onClick={onClick} className={`mood-button ${isActive ? 'active' : ''}`}>
      {moodName}
    </button>
  )
}

export default genreButton