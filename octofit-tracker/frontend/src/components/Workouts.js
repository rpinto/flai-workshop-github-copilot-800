import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts Component - Processed data:', workoutsData);
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts Component - Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      'Beginner': 'bg-success',
      'Intermediate': 'bg-warning',
      'Advanced': 'bg-danger',
      'Expert': 'bg-dark'
    };
    return badges[difficulty] || 'bg-secondary';
  };

  const getWorkoutIcon = (category) => {
    const icons = {
      'Strength': '💪',
      'Cardio': '❤️',
      'Flexibility': '🤸',
      'HIIT': '⚡',
      'Endurance': '🏃',
      'CrossFit': '🏋️'
    };
    return icons[category] || '⚡';
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-container">
          <div className="text-center">
            <div className="spinner-border text-primary" role="status" style={{ width: '3rem', height: '3rem' }}>
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3 text-muted">Loading workouts...</p>
          </div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">⚠️ Error Loading Workouts</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>💪 Workout Suggestions</h2>
      </div>
      <div className="mb-3">
        <h5>Available Workouts: <span className="badge bg-primary">{workouts.length}</span></h5>
      </div>
      <div className="row">
        {workouts.map((workout, index) => (
          <div key={workout.id || index} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-header bg-primary text-white">
                <h5 className="card-title mb-0">
                  {getWorkoutIcon(workout.category)} {workout.name}
                </h5>
              </div>
              <div className="card-body">
                <div className="mb-2">
                  <span className="badge bg-info me-2">{workout.category}</span>
                  <span className={`badge ${getDifficultyBadge(workout.difficulty)}`}>
                    {workout.difficulty}
                  </span>
                </div>
                <p className="card-text">{workout.description}</p>
                
                {workout.exercises && workout.exercises.length > 0 && (
                  <div className="mt-3">
                    <h6 className="fw-bold">Exercises:</h6>
                    <ul className="small">
                      {workout.exercises.map((exercise, idx) => (
                        <li key={idx}>{exercise}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              <ul className="list-group list-group-flush">
                <li className="list-group-item">
                  <strong>⏱️ Duration:</strong> {workout.duration} minutes
                </li>
              </ul>
              <div className="card-footer bg-transparent">
                <button className="btn btn-primary btn-sm w-100">Start Workout</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Workouts;
