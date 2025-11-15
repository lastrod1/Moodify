import React, {useState} from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/authContext'
import './../App.css'

function SignUpPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/auth/sign-up',{
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });
    
    if(response.ok) {
      alert("Login successful");
      navigate('/login');
    }
  }

  return (
    <div className='auth-page'>
      <div className='auth-card'>
        <h2 className='auth-header'>Create Account</h2>
        <form className='auth-form' onSubmit={handleSignUp}>
          <input
            type="text"
            placeholder='Username'
            className="auth-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <input
            type="text"
            placeholder='Password'
            className="auth-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className='auth-button'>
            Sign Up
          </button>
        </form>
        <p className='auth-redirect'>Already a user? <a href='/login'>Login</a></p>
      </div>
    </div>
  )
}

export default SignUpPage