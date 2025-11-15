import React, { useState } from 'react'
import "./../App.css"
import { useAuth } from '../hooks/authContext';
import { useNavigate } from 'react-router-dom';

function LoginPage(){
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, isLoggedIn } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/auth/login', {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    })

    if(response.ok) {
      const loggedIn = await login(username, password);
      if(loggedIn) {
        navigate('/');
      }
    }
  };

  return (
    <div className='auth-page'>
      <div className='auth-card'>
        <h2 className='auth-header'>Login</h2>
        <form className='auth-form' onSubmit={handleLogin}>
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
            Login
          </button>
        </form>
        <p className='auth-redirect'>New User? <a href='/sign-up'>Sign Up</a></p>
      </div>
    </div>
  )
}

export default LoginPage