import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img 
                src="/octofitapp-small.png" 
                alt="OctoFit Logo" 
                className="navbar-logo"
              />
              OctoFit Tracker
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="container-fluid py-4">
          <Routes>
            <Route path="/" element={
              <div className="container">
                <div className="welcome-section text-center">
                  <h1>🏋️ Welcome to OctoFit Tracker</h1>
                  <p className="lead">Track your fitness journey and compete with your team!</p>
                </div>
                
                <div className="row mt-5">
                  <div className="col-md-4 mb-4">
                    <Link to="/users" style={{ textDecoration: 'none' }}>
                      <div className="card h-100 text-center" style={{ cursor: 'pointer' }}>
                        <div className="card-body">
                          <div style={{ fontSize: '4rem' }}>👥</div>
                          <h3 className="card-title mt-3">Users</h3>
                          <p className="card-text">View and manage all registered users</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  
                  <div className="col-md-4 mb-4">
                    <Link to="/activities" style={{ textDecoration: 'none' }}>
                      <div className="card h-100 text-center" style={{ cursor: 'pointer' }}>
                        <div className="card-body">
                          <div style={{ fontSize: '4rem' }}>🎯</div>
                          <h3 className="card-title mt-3">Activities</h3>
                          <p className="card-text">Track all fitness activities and workouts</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  
                  <div className="col-md-4 mb-4">
                    <Link to="/leaderboard" style={{ textDecoration: 'none' }}>
                      <div className="card h-100 text-center" style={{ cursor: 'pointer' }}>
                        <div className="card-body">
                          <div style={{ fontSize: '4rem' }}>📊</div>
                          <h3 className="card-title mt-3">Leaderboard</h3>
                          <p className="card-text">See top performers and rankings</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
                
                <div className="row mt-3">
                  <div className="col-md-6 mb-4">
                    <Link to="/teams" style={{ textDecoration: 'none' }}>
                      <div className="card h-100 text-center" style={{ cursor: 'pointer' }}>
                        <div className="card-body">
                          <div style={{ fontSize: '4rem' }}>🏆</div>
                          <h3 className="card-title mt-3">Teams</h3>
                          <p className="card-text">Manage teams and team members</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  
                  <div className="col-md-6 mb-4">
                    <Link to="/workouts" style={{ textDecoration: 'none' }}>
                      <div className="card h-100 text-center" style={{ cursor: 'pointer' }}>
                        <div className="card-body">
                          <div style={{ fontSize: '4rem' }}>💪</div>
                          <h3 className="card-title mt-3">Workouts</h3>
                          <p className="card-text">Browse personalized workout suggestions</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            } />
            <Route path="/users" element={<Users />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
