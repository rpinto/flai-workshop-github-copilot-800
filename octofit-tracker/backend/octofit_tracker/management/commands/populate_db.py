from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')
        
        # Create unique index on email field using MongoDB directly
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        # Create unique index on email field
        try:
            db.users.create_index([("email", ASCENDING)], unique=True)
            self.stdout.write(self.style.SUCCESS('Created unique index on email field'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Index may already exist: {e}'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing data'))
        
        # Create teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League Champions'
        )
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create users (superheroes)
        self.stdout.write('Creating superhero users...')
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com'},
            {'name': 'Black Panther', 'email': 'tchalla@marvel.com'},
            {'name': 'Doctor Strange', 'email': 'stephen.strange@marvel.com'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com'},
            {'name': 'Cyborg', 'email': 'victor.stone@dc.com'},
            {'name': 'Shazam', 'email': 'billy.batson@dc.com'},
        ]
        
        marvel_users = []
        dc_users = []
        
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_marvel._id)
            )
            marvel_users.append(user)
        
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_dc._id)
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} superhero users'))
        
        # Create activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing', 'Martial Arts']
        activities_count = 0
        
        for user in all_users:
            # Create 5-10 random activities for each user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 12)
                distance = round(random.uniform(1, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                days_ago = random.randint(0, 30)
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    distance=distance,
                    date=datetime.now() - timedelta(days=days_ago)
                )
                activities_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_count} activities'))
        
        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard_entries = []
        
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_activities = user_activities.count()
            total_calories = sum(act.calories for act in user_activities)
            # Points = activities * 10 + calories
            total_points = total_activities * 10 + total_calories
            
            leaderboard_entry = Leaderboard.objects.create(
                user_id=str(user._id),
                team_id=user.team_id,
                total_points=total_points,
                total_activities=total_activities,
                total_calories=total_calories
            )
            leaderboard_entries.append(leaderboard_entry)
        
        # Update ranks
        sorted_entries = sorted(leaderboard_entries, key=lambda x: x.total_points, reverse=True)
        for rank, entry in enumerate(sorted_entries, 1):
            entry.rank = rank
            entry.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries)} leaderboard entries'))
        
        # Create workouts
        self.stdout.write('Creating workout suggestions...')
        workouts_data = [
            {
                'name': 'Avengers Assemble Workout',
                'description': 'A superhero-level full body workout inspired by Earth\'s Mightiest Heroes',
                'difficulty': 'Advanced',
                'duration': 60,
                'category': 'Strength Training',
                'exercises': [
                    {'name': 'Captain America Shield Press', 'sets': 4, 'reps': 12},
                    {'name': 'Thor Hammer Curls', 'sets': 4, 'reps': 10},
                    {'name': 'Hulk Smash Squats', 'sets': 4, 'reps': 15},
                    {'name': 'Black Widow Kicks', 'sets': 3, 'reps': 20}
                ]
            },
            {
                'name': 'Justice League Power Circuit',
                'description': 'High-intensity circuit training like the Justice League',
                'difficulty': 'Advanced',
                'duration': 45,
                'category': 'Circuit Training',
                'exercises': [
                    {'name': 'Superman Flying Push-ups', 'sets': 3, 'reps': 15},
                    {'name': 'Flash Speed Runs', 'sets': 5, 'duration': '30s'},
                    {'name': 'Wonder Woman Lasso Pulls', 'sets': 4, 'reps': 12},
                    {'name': 'Aquaman Swimming Strokes', 'sets': 3, 'reps': 20}
                ]
            },
            {
                'name': 'Spider-Man Agility Training',
                'description': 'Web-swinging agility and flexibility workout',
                'difficulty': 'Intermediate',
                'duration': 40,
                'category': 'Agility',
                'exercises': [
                    {'name': 'Wall Crawl Planks', 'sets': 3, 'duration': '60s'},
                    {'name': 'Web-Shooter Burpees', 'sets': 4, 'reps': 15},
                    {'name': 'Spider Sense Jumps', 'sets': 3, 'reps': 20},
                    {'name': 'Web-Swing Stretches', 'sets': 2, 'duration': '90s'}
                ]
            },
            {
                'name': 'Batman Dark Knight Cardio',
                'description': 'Gotham\'s guardian nocturnal cardio session',
                'difficulty': 'Intermediate',
                'duration': 35,
                'category': 'Cardio',
                'exercises': [
                    {'name': 'Batcave Running', 'duration': '10min'},
                    {'name': 'Grappling Hook Pulls', 'sets': 4, 'reps': 12},
                    {'name': 'Rooftop Jumping Jacks', 'sets': 3, 'reps': 25},
                    {'name': 'Batarang Throws', 'sets': 3, 'reps': 15}
                ]
            },
            {
                'name': 'Iron Man Reactor Core',
                'description': 'Core strengthening for arc reactor power',
                'difficulty': 'Beginner',
                'duration': 30,
                'category': 'Core',
                'exercises': [
                    {'name': 'Arc Reactor Crunches', 'sets': 3, 'reps': 20},
                    {'name': 'Repulsor Blast Twists', 'sets': 3, 'reps': 15},
                    {'name': 'Flight Stabilizer Planks', 'sets': 3, 'duration': '45s'},
                    {'name': 'Jarvis Leg Raises', 'sets': 3, 'reps': 15}
                ]
            },
            {
                'name': 'Black Panther Wakanda Warrior',
                'description': 'Traditional Wakandan combat training',
                'difficulty': 'Advanced',
                'duration': 50,
                'category': 'Martial Arts',
                'exercises': [
                    {'name': 'Vibranium Shield Blocks', 'sets': 4, 'reps': 20},
                    {'name': 'Panther Strike Combos', 'sets': 4, 'reps': 15},
                    {'name': 'Dora Milaje Spear Thrusts', 'sets': 3, 'reps': 18},
                    {'name': 'Wakandan Jump Kicks', 'sets': 3, 'reps': 12}
                ]
            }
        ]
        
        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts_data)} workout suggestions'))
        
        # Final summary
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
