import React from 'react'
import "./genreButton.css"

function genreButton({ genreName }) {
  return (
    <button class="genre-button">
      {genreName}
    </button>
  )
}

export default genreButton