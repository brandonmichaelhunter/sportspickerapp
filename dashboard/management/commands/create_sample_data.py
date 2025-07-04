from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from dashboard.models import Sport, Team, Game, UserPick
import random


class Command(BaseCommand):
    help = 'Create sample data for the Sports Picker app'

    def handle(self, *args, **options):
        # Create sports
        football = Sport.objects.get_or_create(
            name='Football',
            defaults={'description': 'American Football'}
        )[0]
        
        basketball = Sport.objects.get_or_create(
            name='Basketball',
            defaults={'description': 'Professional Basketball'}
        )[0]
        
        # Create football teams
        football_teams = [
            ('Dallas', 'Cowboys', 8, 4, 0),
            ('Green Bay', 'Packers', 7, 5, 0),
            ('New England', 'Patriots', 6, 6, 0),
            ('Pittsburgh', 'Steelers', 9, 3, 0),
            ('Kansas City', 'Chiefs', 10, 2, 0),
            ('Buffalo', 'Bills', 8, 4, 0),
            ('Miami', 'Dolphins', 5, 7, 0),
            ('New York', 'Giants', 4, 8, 0),
        ]
        
        for city, name, wins, losses, ties in football_teams:
            Team.objects.get_or_create(
                name=name,
                city=city,
                sport=football,
                defaults={'wins': wins, 'losses': losses, 'ties': ties}
            )
        
        # Create basketball teams
        basketball_teams = [
            ('Los Angeles', 'Lakers', 25, 15, 0),
            ('Boston', 'Celtics', 28, 12, 0),
            ('Golden State', 'Warriors', 22, 18, 0),
            ('Miami', 'Heat', 20, 20, 0),
            ('Chicago', 'Bulls', 18, 22, 0),
            ('Phoenix', 'Suns', 24, 16, 0),
        ]
        
        for city, name, wins, losses, ties in basketball_teams:
            Team.objects.get_or_create(
                name=name,
                city=city,
                sport=basketball,
                defaults={'wins': wins, 'losses': losses, 'ties': ties}
            )
        
        # Create some games
        now = datetime.now()
        locations = [
            'MetLife Stadium', 'Lambeau Field', 'Gillette Stadium', 
            'Heinz Field', 'Arrowhead Stadium', 'Highmark Stadium',
            'Staples Center', 'TD Garden', 'Chase Center', 
            'FTX Arena', 'United Center', 'Phoenix Suns Arena'
        ]
        
        # Football games
        football_teams_list = list(Team.objects.filter(sport=football))
        for i in range(10):
            home_team = random.choice(football_teams_list)
            away_team = random.choice([t for t in football_teams_list if t != home_team])
            
            game_date = now + timedelta(days=random.randint(-7, 14))
            location = random.choice(locations[:6])  # Football stadiums
            
            game, created = Game.objects.get_or_create(
                home_team=home_team,
                away_team=away_team,
                game_date=game_date,
                defaults={
                    'location': location,
                    'sport': football,
                }
            )
            
            # Some games are completed
            if random.random() < 0.3:
                game.is_completed = True
                game.home_score = random.randint(0, 35)
                game.away_score = random.randint(0, 35)
                game.save()
        
        # Basketball games
        basketball_teams_list = list(Team.objects.filter(sport=basketball))
        for i in range(8):
            home_team = random.choice(basketball_teams_list)
            away_team = random.choice([t for t in basketball_teams_list if t != home_team])
            
            game_date = now + timedelta(days=random.randint(-3, 7))
            location = random.choice(locations[6:])  # Basketball arenas
            
            game, created = Game.objects.get_or_create(
                home_team=home_team,
                away_team=away_team,
                game_date=game_date,
                defaults={
                    'location': location,
                    'sport': basketball,
                }
            )
            
            # Some games are completed
            if random.random() < 0.4:
                game.is_completed = True
                game.home_score = random.randint(80, 120)
                game.away_score = random.randint(80, 120)
                game.save()
        
        # Create some sample users and picks
        test_users = []
        for i in range(5):
            username = f'user{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Test',
                    'last_name': f'User{i+1}'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            test_users.append(user)
        
        # Create random picks for upcoming games
        upcoming_games = Game.objects.filter(is_completed=False)
        for user in test_users:
            for game in random.sample(list(upcoming_games), min(len(upcoming_games), random.randint(2, 5))):
                pick_choice = random.choice(['HOME', 'AWAY', 'TIE'])
                UserPick.objects.get_or_create(
                    user=user,
                    game=game,
                    defaults={'pick': pick_choice}
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )