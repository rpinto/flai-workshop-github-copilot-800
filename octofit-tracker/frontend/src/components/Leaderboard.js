import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
  const USERS_API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
  const TEAMS_API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Leaderboard Component - Fetching from:', API_URL);
    
    // Fetch leaderboard, users, and teams data
    Promise.all([
      fetch(API_URL).then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      }),
      fetch(USERS_API_URL).then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      }),
      fetch(TEAMS_API_URL).then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
    ])
      .then(([leaderboardData, usersData, teamsData]) => {
        console.log('Leaderboard Component - Raw leaderboard data received:', leaderboardData);
        console.log('Leaderboard Component - Raw users data received:', usersData);
        console.log('Leaderboard Component - Raw teams data received:', teamsData);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboard = leaderboardData.results || leaderboardData;
        const users = usersData.results || usersData;
        const teams = teamsData.results || teamsData;
        
        console.log('Leaderboard Component - Processed leaderboard:', leaderboard);
        console.log('Leaderboard Component - Processed users:', users);
        console.log('Leaderboard Component - Processed teams:', teams);
        
        setLeaderboard(leaderboard);
        setUsers(users);
        setTeams(teams);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL, USERS_API_URL, TEAMS_API_URL]);

  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? user.name : `User ${userId}`;
  };

  const getTeamName = (teamId) => {
    if (!teamId) return 'N/A';
    const team = teams.find(t => t.id === teamId);
    return team ? team.name : 'N/A';
  };

  const getRankBadgeClass = (rank) => {
    if (rank === 1) return 'rank-badge rank-1';
    if (rank === 2) return 'rank-badge rank-2';
    if (rank === 3) return 'rank-badge rank-3';
    return 'rank-badge rank-other';
  };

  const getRankEmoji = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-container">
          <div className="text-center">
            <div className="spinner-border text-warning" role="status" style={{ width: '3rem', height: '3rem' }}>
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3 text-muted">Loading leaderboard...</p>
          </div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">⚠️ Error Loading Leaderboard</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>📊 Leaderboard</h2>
      </div>
      <div className="table-container">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">Top Performers</h5>
        </div>
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Rank</th>
                <th>User</th>
                <th>Team</th>
                <th>Total Points</th>
                <th>Total Activities</th>
                <th>Total Calories</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr key={entry.id || index} className={entry.rank <= 3 ? 'table-warning' : ''}>
                  <td>
                    <div className={getRankBadgeClass(entry.rank)}>
                      {getRankEmoji(entry.rank)}
                    </div>
                  </td>
                  <td><strong>{getUserName(entry.user_id)}</strong></td>
                  <td>
                    <span className="badge bg-info">{getTeamName(entry.team_id)}</span>
                  </td>
                  <td>
                    <span className="badge bg-success">{entry.total_points} pts</span>
                  </td>
                  <td>
                    <span className="badge bg-primary">{entry.total_activities} activities</span>
                  </td>
                  <td>
                    <span className="badge bg-danger">{entry.total_calories} cal</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
