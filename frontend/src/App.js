import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import SignUpPage from './pages/SignUpPage';
import ProfilePage from './pages/ProfilePage';
import { useAuth } from './hooks/authContext'
import './App.css'; 

function App() {
    const { isLoggedIn } = useAuth();
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/sign-up" element={<SignUpPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route 
                    path="/" 
                    element={isLoggedIn ? (<HomePage/>) : <Navigate to="/login" replace/>} 
                />
            </Routes>
        </Router>
    );
}

export default App;