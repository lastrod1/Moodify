import React from 'react'
import "./moodButton.css"

function genreButton({ moodName }) {
  return (
    <button class="mood-button">
      {moodName}
    </button>
  )
}

export default genreButton