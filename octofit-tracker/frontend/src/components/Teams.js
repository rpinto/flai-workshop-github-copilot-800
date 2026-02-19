import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
  const USERS_API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;

  useEffect(() => {
    console.log('Teams Component - Fetching from:', API_URL);
    
    // Fetch both teams and users
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
      })
    ])
      .then(([teamsData, usersData]) => {
        console.log('Teams Component - Raw teams data received:', teamsData);
        console.log('Teams Component - Raw users data received:', usersData);
        
        // Handle both paginated (.results) and plain array responses
        const teams = teamsData.results || teamsData;
        const users = usersData.results || usersData;
        
        console.log('Teams Component - Processed teams:', teams);
        console.log('Teams Component - Processed users:', users);
        
        setTeams(teams);
        setUsers(users);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL, USERS_API_URL]);

  const getTeamMembers = (teamId) => {
    return users.filter(user => user.team_id === teamId);
  };

  const getTeamMemberCount = (teamId) => {
    return users.filter(user => user.team_id === teamId).length;
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-container">
          <div className="text-center">
            <div className="spinner-border text-success" role="status" style={{ width: '3rem', height: '3rem' }}>
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3 text-muted">Loading teams...</p>
          </div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">⚠️ Error Loading Teams</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>🏆 Teams</h2>
      </div>
      <div className="mb-3">
        <h5>Total Teams: <span className="badge bg-success">{teams.length}</span></h5>
      </div>
      <div className="row">
        {teams.map((team, index) => {
          const teamMembers = getTeamMembers(team.id);
          const memberCount = getTeamMemberCount(team.id);
          
          return (
            <div key={team.id || index} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-header bg-success text-white">
                  <h5 className="card-title mb-0">{team.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">{team.description}</p>
                  <div className="d-flex align-items-center mb-3">
                    <span className="badge bg-info me-2">👥 {memberCount} members</span>
                  </div>
                  {teamMembers.length > 0 && (
                    <div>
                      <h6 className="fw-bold">Team Members:</h6>
                      <ul className="list-group list-group-flush">
                        {teamMembers.map((member, idx) => (
                          <li key={member.id || idx} className="list-group-item px-0">✓ {member.name}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Teams;
