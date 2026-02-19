from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm
from .models import UserProfile, UserLanguage, Language
from srs.models import SRSCard
from stats.models import DailyActivity


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                target_country=form.cleaned_data['target_country'],
            )

            for lang_code in form.cleaned_data['target_languages']:
                lang, _ = Language.objects.get_or_create(
                    code=lang_code,
                    defaults={'name': 'English' if lang_code == 'en' else 'German'}
                )
                level = form.cleaned_data.get(f'current_level_{lang_code}') or 'A1'
                UserLanguage.objects.create(user=user, language=lang, current_level=level)

            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Let's start learning.")
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    today = date.today()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_langs = request.user.user_languages.select_related('language').filter(is_active=True)

    cards_due = SRSCard.objects.filter(
        user=request.user,
        next_review_date__lte=today
    ).count()

    cards_total = SRSCard.objects.filter(user=request.user).count()
    cards_learned = SRSCard.objects.filter(user=request.user, repetitions__gte=3).count()

    today_activity, _ = DailyActivity.objects.get_or_create(
        user=request.user, activity_date=today
    )

    recent_activity = DailyActivity.objects.filter(
        user=request.user
    ).order_by('-activity_date')[:7]

    context = {
        'profile': profile,
        'user_langs': user_langs,
        'cards_due': cards_due,
        'cards_total': cards_total,
        'cards_learned': cards_learned,
        'today_activity': today_activity,
        'recent_activity': recent_activity,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_langs = request.user.user_languages.select_related('language').filter(is_active=True)

    if request.method == 'POST':
        profile.target_country = request.POST.get('target_country', profile.target_country)
        profile.daily_goal_minutes = int(request.POST.get('daily_goal_minutes', 10))
        profile.save()

        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        messages.success(request, 'Profile updated.')
        return redirect('profile')

    return render(request, 'core/profile.html', {
        'profile': profile,
        'user_langs': user_langs,
    })
