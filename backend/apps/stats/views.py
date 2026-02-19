from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DailyActivity


@login_required
def progress_view(request):
    activities = DailyActivity.objects.filter(user=request.user).order_by('-activity_date')[:30]
    total_xp = sum(a.xp_earned for a in activities)
    total_cards = sum(a.cards_reviewed for a in activities)

    return render(request, 'stats/progress.html', {
        'activities': activities,
        'total_xp': total_xp,
        'total_cards': total_cards,
        'streak': request.user.profile.current_streak,
        'longest_streak': request.user.profile.longest_streak,
    })
