import React, { useState } from 'react'
import { useAuth } from './../hooks/authContext'
import { useNavigate } from 'react-router-dom';
import './../App.css'
function ProfilePage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isUpdating, setIsUpdating] = useState(false);
    const [message, setMessage] = useState('')
    const { user, setUser } = useAuth();
    const navigate = useNavigate();


    const handleProfileChange = async (e) => {
        e.preventDefault();
        setIsUpdating(true);
        setMessage('')

        const updateData = {};
        if(username.trim()){
            updateData.username = username.trim();
        }
        if(password.trim()){
            updateData.password = password.trim();
        }

        if(Object.keys(updateData).length === 0) {
            setMessage('Please enter a new username or password');
            setIsUpdating(false);
            return;
        }

        try {
            const response = await fetch('/api/auth/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': user.username
                },
                body: JSON.stringify(updateData),
            });

            const result = await response.json();
            if(response.ok) {
                setMessage(result.message);
                
                if(result.new_username) {
                    setUser({ ...user, username: result.new_username})
                }

                setUsername('');
                setPassword('');
            } else {
                setMessage(`Error: ${result.error || result.message}`);
            }
        } catch(error) {
            console.error("Network or fetch error:", error);
            setMessage('An unexpected error occurred. Please try again.');
        } finally {
            setIsUpdating(false);
        }
    }

    const handleProfileDelete = async (e) => {
        const response = await fetch('/api/auth/delete', {
            method: 'DELETE',
            headers: {
                'Authorization': user.username
            },
        });
        navigate('/login');
    }

  return (
    <div className='auth-page'>
        <div className='auth-card'>
            <h2 className='auth-header'>Profile Change</h2>
            <form className='auth-form' onSubmit={handleProfileChange}>
            <input
                type="text"
                placeholder='Username'
                className="auth-input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                type="text"
                placeholder='Password'
                className="auth-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit" className='auth-button'>
                Change Credentials
            </button>
            </form>
            <button className='delete-button' onClick={handleProfileDelete}>
                Delete Account
            </button>
        </div>
    </div>
  )
}

export default ProfilePage