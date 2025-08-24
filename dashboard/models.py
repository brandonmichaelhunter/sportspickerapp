from django.db import models
from django.contrib.auth.models import User


class Sport(models.Model):
    """Model representing different sports"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Team(models.Model):
    """Model representing sports teams"""
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['name', 'city', 'sport']
    
    def __str__(self):
        return f"{self.city} {self.name}"
    
    @property
    def record(self):
        return f"{self.wins}-{self.losses}-{self.ties}"


class Game(models.Model):
    """Model representing games between teams"""
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    game_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    
    # Game result (null if game hasn't been played yet)
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['home_team', 'away_team', 'game_date']
    
    def __str__(self):
        return f"{self.away_team} @ {self.home_team} - {self.game_date.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def winner(self):
        if not self.is_completed or self.home_score is None or self.away_score is None:
            return None
        if self.home_score > self.away_score:
            return self.home_team
        elif self.away_score > self.home_score:
            return self.away_team
        else:
            return "TIE"


class UserPick(models.Model):
    """Model representing user predictions for games"""
    PICK_CHOICES = [
        ('HOME', 'Home Team Wins'),
        ('AWAY', 'Away Team Wins'),
        ('TIE', 'Tie'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    pick = models.CharField(max_length=4, choices=PICK_CHOICES)
    pick_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'game']
    
    def __str__(self):
        return f"{self.user.username} picks {self.get_pick_display()} for {self.game}"
