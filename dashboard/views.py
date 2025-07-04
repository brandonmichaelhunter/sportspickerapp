from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Sport, Team, Game, UserPick


def dashboard(request):
    """Main dashboard view"""
    sports = Sport.objects.all()
    selected_sport_id = request.GET.get('sport')
    selected_team_id = request.GET.get('team')
    view_period = request.GET.get('period', 'week')  # week, day, month
    
    context = {
        'sports': sports,
        'selected_sport_id': selected_sport_id,
        'selected_team_id': selected_team_id,
        'view_period': view_period,
    }
    
    # Filter teams by selected sport
    if selected_sport_id:
        selected_sport = get_object_or_404(Sport, id=selected_sport_id)
        teams = Team.objects.filter(sport=selected_sport)
        context['selected_sport'] = selected_sport
        context['teams'] = teams
        
        # Get games based on view period and filters
        games = Game.objects.filter(sport=selected_sport)
        
        # Filter by team if selected
        if selected_team_id:
            selected_team = get_object_or_404(Team, id=selected_team_id)
            games = games.filter(Q(home_team=selected_team) | Q(away_team=selected_team))
            context['selected_team'] = selected_team
        
        # Filter by time period
        today = datetime.now().date()
        if view_period == 'day':
            games = games.filter(game_date__date=today)
        elif view_period == 'week':
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            games = games.filter(game_date__date__range=[start_week, end_week])
        elif view_period == 'month':
            games = games.filter(
                game_date__year=today.year,
                game_date__month=today.month
            )
        
        # Annotate games with pick statistics
        games = games.annotate(
            total_picks=Count('userpick'),
            home_picks=Count('userpick', filter=Q(userpick__pick='HOME')),
            away_picks=Count('userpick', filter=Q(userpick__pick='AWAY')),
            tie_picks=Count('userpick', filter=Q(userpick__pick='TIE'))
        ).order_by('game_date')
        
        context['games'] = games
    
    return render(request, 'dashboard/dashboard.html', context)


def get_game_history(request, game_id):
    """Get historical games between two teams"""
    game = get_object_or_404(Game, id=game_id)
    
    # Get past games between these two teams
    historical_games = Game.objects.filter(
        Q(home_team=game.home_team, away_team=game.away_team) |
        Q(home_team=game.away_team, away_team=game.home_team),
        is_completed=True,
        game_date__lt=game.game_date
    ).order_by('-game_date')[:10]  # Last 10 games
    
    history_data = []
    for hist_game in historical_games:
        history_data.append({
            'date': hist_game.game_date.strftime('%Y-%m-%d'),
            'home_team': str(hist_game.home_team),
            'away_team': str(hist_game.away_team),
            'home_score': hist_game.home_score,
            'away_score': hist_game.away_score,
            'winner': str(hist_game.winner) if hist_game.winner else 'TIE'
        })
    
    return JsonResponse({'history': history_data})


@login_required
def make_pick(request, game_id):
    """Allow user to make a pick for a game"""
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        pick_choice = request.POST.get('pick')
        
        if pick_choice in ['HOME', 'AWAY', 'TIE']:
            user_pick, created = UserPick.objects.get_or_create(
                user=request.user,
                game=game,
                defaults={'pick': pick_choice}
            )
            if not created:
                user_pick.pick = pick_choice
                user_pick.save()
            
            return JsonResponse({'success': True, 'message': 'Pick saved successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def chatbot_response(request):
    """Simple chatbot for team questions"""
    question = request.GET.get('question', '').lower()
    team_id = request.GET.get('team_id')
    
    response = "I'm a simple chatbot. Ask me about team records, recent games, or general information!"
    
    if team_id:
        try:
            team = Team.objects.get(id=team_id)
            if 'record' in question or 'win' in question or 'loss' in question:
                response = f"{team.name} current record is {team.record} (Wins-Losses-Ties)."
            elif 'recent' in question or 'last' in question:
                recent_games = Game.objects.filter(
                    Q(home_team=team) | Q(away_team=team),
                    is_completed=True
                ).order_by('-game_date')[:3]
                
                if recent_games:
                    games_text = []
                    for game in recent_games:
                        games_text.append(f"{game.away_team} {game.away_score} - {game.home_score} {game.home_team}")
                    response = f"Recent games for {team.name}: " + "; ".join(games_text)
                else:
                    response = f"No recent completed games found for {team.name}."
            else:
                response = f"You asked about {team.name}. Ask me about their record or recent games!"
        except Team.DoesNotExist:
            response = "Team not found."
    
    return JsonResponse({'response': response})
