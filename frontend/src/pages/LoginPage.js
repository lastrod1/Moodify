import React from 'react'
import './../App.css'

function LoginPage() {
  return (
    <div className='login-page'>
        <div className='login-container'>
            <h2 className='app-name'>Moodify</h2>
            <a className='sign-up-link' href='http://localhost:3000/sign-up'>Sign Up</a>
        </div>
    </div>
  )
}

export default LoginPage