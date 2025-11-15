import React, {useState} from 'react'
import { useAuth } from '../hooks/authContext'
import './../App.css'

function SignUpPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const { login } = useAuth();

  return (
    <div className='signup-page'>
      <div className='signup-card'>
        <h2 className='signup-header'>Create Account</h2>
        <form className='signup-form'>
          <input
            type="text"
            placeholder='Username'
            className="signup-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <input
            type="text"
            placeholder='Password'
            className="signup-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className='signup-button'>
            Sign Up
          </button>
        </form>
        <p className='signup-redirect'>Already a user? <a href='/login'>Login</a></p>
      </div>
    </div>
  )
}

export default SignUpPage