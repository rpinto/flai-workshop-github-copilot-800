from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserAPITestCase(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'team_id': None
        }
        self.user = User.objects.create(**self.user_data)
    
    def test_get_users_list(self):
        """Test retrieving users list"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list')
        new_user_data = {
            'name': 'New User',
            'email': 'newuser@example.com'
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_user_data['name'])
    
    def test_get_user_by_email(self):
        """Test getting user by email"""
        url = reverse('user-by-email')
        response = self.client.get(url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)


class TeamAPITestCase(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'Test Team',
            'description': 'A test team'
        }
        self.team = Team.objects.create(**self.team_data)
    
    def test_get_teams_list(self):
        """Test retrieving teams list"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_team(self):
        """Test creating a new team"""
        url = reverse('team-list')
        new_team_data = {
            'name': 'New Team',
            'description': 'A new test team'
        }
        response = self.client.post(url, new_team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_team_data['name'])


class ActivityAPITestCase(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name='Test User', email='test@example.com')
        self.activity_data = {
            'user_id': str(self.user._id),
            'activity_type': 'Running',
            'duration': 30,
            'calories': 300,
            'distance': 5.0,
            'date': datetime.now()
        }
        self.activity = Activity.objects.create(**self.activity_data)
    
    def test_get_activities_list(self):
        """Test retrieving activities list"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        url = reverse('activity-list')
        new_activity_data = {
            'user_id': str(self.user._id),
            'activity_type': 'Cycling',
            'duration': 45,
            'calories': 400,
            'distance': 15.0,
            'date': datetime.now().isoformat()
        }
        response = self.client.post(url, new_activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaderboardAPITestCase(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name='Test User', email='test@example.com')
        self.leaderboard_data = {
            'user_id': str(self.user._id),
            'total_points': 100,
            'total_activities': 10,
            'total_calories': 1000,
            'rank': 1
        }
        self.leaderboard = Leaderboard.objects.create(**self.leaderboard_data)
    
    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard list"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_top_leaderboard(self):
        """Test getting top entries from leaderboard"""
        url = reverse('leaderboard-top')
        response = self.client.get(url, {'limit': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 5)


class WorkoutAPITestCase(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Test Workout',
            'description': 'A test workout routine',
            'difficulty': 'intermediate',
            'duration': 30,
            'category': 'strength',
            'exercises': [
                {'name': 'Push-ups', 'reps': 20},
                {'name': 'Squats', 'reps': 15}
            ]
        }
        self.workout = Workout.objects.create(**self.workout_data)
    
    def test_get_workouts_list(self):
        """Test retrieving workouts list"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        url = reverse('workout-list')
        new_workout_data = {
            'name': 'New Workout',
            'description': 'A new test workout',
            'difficulty': 'beginner',
            'duration': 20,
            'category': 'cardio',
            'exercises': []
        }
        response = self.client.post(url, new_workout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_workout_data['name'])
    
    def test_get_workouts_by_difficulty(self):
        """Test filtering workouts by difficulty"""
        url = reverse('workout-by-difficulty')
        response = self.client.get(url, {'difficulty': 'intermediate'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
