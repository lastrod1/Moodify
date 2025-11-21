import React from 'react'

function songBar({song_title, artist}) {
  return (
    <div className='song-bar'>
        <p className='song-title'>{song_title}</p>
        <p className='artist'>{artist}</p>
    </div>
  )
}

export default songBar